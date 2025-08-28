import streamlit as st
import os
from pathlib import Path
import cv2
import numpy as np
import fitz
from typing import List
import base64
from docx2pdf import convert
import tempfile

# === Import your OCR & TTS classes ===
from src.ocr.mistral_ocr import ocr_mistral   
from src.ocr.paddle_ocr import PaddleOCREngine
from src.tts.gtts_engine import GTTSEngine
from src.preprocessing.image_preprocessing import preprocess_pipeline


# --- Document Loader ---
def load_document(uploaded_file) -> List[str]:
    """
    Load uploaded document (pdf, docx, image) from Streamlit 
    and return list of base64-encoded images.
    """
    file_suffix = Path(uploaded_file.name).suffix.lower()

    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=file_suffix) as tmp_file:
        tmp_file.write(uploaded_file.read())
        tmp_path = Path(tmp_file.name)

    if file_suffix == ".pdf":
        return load_pdf(tmp_path)
    
    elif file_suffix == ".docx":
        convert(tmp_path)  # Convert DOCX -> PDF
        return load_pdf(tmp_path.with_suffix(".pdf"))
    
    elif file_suffix in [".png", ".jpg", ".jpeg"]:
        # Read image
        img = cv2.imdecode(np.frombuffer(tmp_path.read_bytes(), np.uint8), cv2.IMREAD_COLOR)
        processed = preprocess_pipeline(img)
        _, buffer = cv2.imencode(".png", processed)
        base64_img = base64.b64encode(buffer).decode("utf-8")
        return [base64_img]

    else:
        raise ValueError(f"Unsupported file format: {file_suffix}")
    
def load_pdf(pdf_path: Path) -> List[str]:
    """Convert PDF to preprocessed base64-encoded images."""
    doc = fitz.open(pdf_path)
    base64_images = []

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))

        # Convert pixmap → numpy
        img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)

        if pix.n == 4:
            img = cv2.cvtColor(img, cv2.COLOR_RGBA2BGR)
        elif pix.n == 3:
            img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

        processed = preprocess_pipeline(img)
        _, buffer = cv2.imencode(".png", processed)
        base64_img = base64.b64encode(buffer).decode("utf-8")
        base64_images.append(base64_img)

    doc.close()
    return base64_images



# --- App Config ---
st.set_page_config(page_title="OCR + TTS App", page_icon="🎤", layout="centered")

# === Sidebar ===
st.sidebar.title("Settings")
language = st.sidebar.selectbox("TTS Language", ["ar", "en"])
slow = st.sidebar.checkbox("Slow speech", False)

# === Title ===
st.title("📖 OCR + 🎤 TTS Demo")
st.write("Upload an image, extract text with OCR, and listen to the audio.")

# === File Upload ===
uploaded_file = st.file_uploader("Upload a file", type=["pdf", "docx", "png", "jpg", "jpeg"])

if uploaded_file:
    # === Run OCR ===
    st.subheader("📖 Extracted Text")
    ocr_engine = ocr_mistral({"api_key": "T0lbb5RDSkMCbHsrPRyCjsJ7czOYCxMs"})  # replace with your config
    images = load_document(uploaded_file)

    all_text = []
    for img_b64 in images:
        text_results = ocr_engine.extract_text(img_b64)  # <-- pass base64 string

        if text_results:
            page_text = " ".join([tr.text for tr in text_results])
            all_text.append(page_text)

    extracted_text = "\n".join(all_text)
    st.text_area("OCR Output", extracted_text, height=200)

    # === Run TTS ===
    if extracted_text.strip():
        st.subheader("🎤 Text-to-Speech")
        tts_engine = GTTSEngine({"language": language, "slow": slow})
        output_path = "output_audio.mp3"
        tts_result = tts_engine.synthesize(extracted_text, output_path)

        # Play audio
        audio_bytes = open(output_path, "rb").read()
        st.audio(audio_bytes, format="audio/mp3")
