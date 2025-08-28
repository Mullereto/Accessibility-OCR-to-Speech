import logging
from typing import Dict, Any, List
from .base_ocr import BaseOCREngine, TextResult
import cv2
import numpy as np
import base64


class PaddleOCREngine(BaseOCREngine):
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.logger = logging.getLogger(__name__)
        self._initialize_engine()
        
    def _initialize_engine(self):
        try:
            from paddleocr import PaddleOCR
            self.ocr = PaddleOCR(
                use_angle_cls=self.config.get("use_angle_cls", True),
                lang=self.config.get("language", "ar"),
                # use_gpu is not a valid parameter, removing it
            )
            self.logger.info("PaddleOCR engine initialized successfully")
        except ImportError as e:
            self.logger.error(f"Failed to initialize PaddleOCR engine: {e}")
            raise
    def extract_text(self, image_path:str) -> str:
        try:
            result = self.ocr.predict(image_path)
            text = ' '.join([line[1][0] for line in result[0] if line[1][1] > self.config.get("confidence_threshold", 0.7)])
            self.logger.info(f"Extracted {len(text)} characters from {image_path}")
            return text
        except Exception as e:
            self.logger.error(f"OCR extraction failed: {e}")
            raise
    def extract_text_with_confidence(self, image_path: str) -> List[TextResult]:
        try:
            # Decode Base64 string -> bytes
            img_bytes = base64.b64decode(image_path)

            # Bytes -> NumPy array
            nparr = np.frombuffer(img_bytes, np.uint8)

            # NumPy -> OpenCV image
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            results = self.ocr.predict(img)

            text_results = []

            for res in results:
                # PaddleOCR classic mode (list of [coords, (text, conf)])
                for text, conf, bbox in zip(res["rec_texts"], res["rec_scores"], res["rec_boxes"]):
                    if conf > self.config.get("confidence_threshold", 0.7):
                        text_results.append(TextResult(
                            text=text[::-1] if self.config['language'] == "ar" else text,

                            confidence=conf,
                            bbox=bbox.tolist() if bbox is not None else None,

                            language=self.config.get("language", "ar")
                        ))
            return text_results
        except Exception as e:
            self.logger.error(f"OCR extraction with confidence failed: {e}")
            raise
    def is_available(self, image_path:str) -> bool:
        try:
            self.ocr.predict(image_path)
            return True
        except Exception as e:
            self.logger.error(f"Failed to extract text from image: {e}")
            return False