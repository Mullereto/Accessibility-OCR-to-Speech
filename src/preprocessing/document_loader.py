import logging
from typing import List
from pathlib import Path
import fitz  # PyMuPDF
from docx2pdf import convert
import base64
import cv2

from .image_preprocessing import preprocess_pipeline
import numpy as np

logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    )


class DocumentLoader:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def load_document(self, file_path:str) -> List[str]:
        """Load document and return list of image paths."""
        file_path = Path(file_path)
        if file_path.suffix == ".pdf":
            return self._load_pdf(file_path)
        elif file_path.suffix == ".docx":
            convert(file_path)
            return self._load_pdf(file_path)
        elif file_path.suffix.lower() in ['.png', '.jpg', '.jpeg']:
                img = cv2.imread(str(file_path))
                processed = preprocess_pipeline(img)
                _, buffer = cv2.imencode(".png", processed)
                base64_img = base64.b64encode(buffer).decode("utf-8")
                return [base64_img]

        else:
            raise ValueError(f"Unsupported file format: {file_path.suffix}")

         
    
    def _load_pdf(self, pdf_path: Path) -> List[str]:
        """Convert PDF to preprocessed base64-encoded images."""
        try:
            self.logger.info(f"Loading PDF: {pdf_path}")
            doc = fitz.open(pdf_path)
            base64_images = []

            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))

                # Convert pixmap to numpy
                img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)

                # Convert color channels
                if pix.n == 4:
                    img = cv2.cvtColor(img, cv2.COLOR_RGBA2BGR)
                elif pix.n == 3:
                    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

                # Apply preprocessing
                processed = preprocess_pipeline(img)

                # Encode processed image as base64 (no file save needed)
                _, buffer = cv2.imencode(".png", processed)
                base64_img = base64.b64encode(buffer).decode("utf-8")

                base64_images.append(base64_img)
                self.logger.info(f"Converted and preprocessed page {page_num+1}")

            doc.close()
            return base64_images


        except Exception as e:
            self.logger.error(f"PDF loading failed: {e}")
            raise