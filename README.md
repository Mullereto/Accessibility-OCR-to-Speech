# 📖 OCR + 🎤 TTS Project

This project is an **OCR (Optical Character Recognition) + TTS (Text-to-Speech)** pipeline that allows users to upload PDFs, DOCX, or images, extract text using OCR, and listen to it with a TTS engine.  
The project also includes a **Streamlit web app** for an interactive user experience.

---

## 🚀 Features

- 📂 Supports **PDF, DOCX, PNG, JPG, JPEG** uploads  
- 🔍 OCR using:
  - [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR)
  - [Mistral API](https://mistral.ai/)  
- 🎤 TTS using:
  - [gTTS](https://pypi.org/project/gTTS/) (Google Text-to-Speech)  
- 🖼️ Preprocessing pipeline with **OpenCV** for better OCR results  
- 🌐 Interactive **Streamlit App**  
- 🔊 Supports **Arabic and English text-to-speech**  


---

## ⚙️ Installation

1. Clone the repository:

```bash
git clone https://github.com/your-username/ocr-tts-project.git
cd ocr-tts-project
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate   # On Linux/Mac
venv\Scripts\activate      # On Windows
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

---

## ▶️ Usage

### Run the Streamlit App

```bash
streamlit run app.py
```

### Steps in the App
1. Upload a file (**PDF, DOCX, or image**)  
2. Extract text with OCR  
3. Convert text to **speech (TTS)**  
4. Listen or download the audio  

---

## 🧰 Dependencies

- Python 3.9+  
- [Streamlit](https://streamlit.io/)  
- [OpenCV](https://opencv.org/)  
- [PyMuPDF (fitz)](https://pymupdf.readthedocs.io/en/latest/)  
- [gTTS](https://pypi.org/project/gTTS/)  
- [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR)  
- [docx2pdf](https://pypi.org/project/docx2pdf/)  
- NumPy  

Install them via:

```bash
pip install -r requirements.txt
```

