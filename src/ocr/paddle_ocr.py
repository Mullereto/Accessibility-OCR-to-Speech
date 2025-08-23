import logging
from typing import Dict, Any, List
from .base_ocr import BaseOCREngine, TextResult


class PaddleOCREngine(BaseOCREngine):
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.logger = logging.getLogger(__name__)
        self._initialize_engine()
        
    def _initialize_engine(self):
        try:
            from paddleocr import PaddleOCR
            import cv2
            self.ocr = PaddleOCR(
                use_angle_cls=self.config.get("use_angle_cls", True),
                lang=self.config.get("language", "ar"),
                use_gpu=self.config.get("use_gpu", False),

            )
            self.logger.info("PaddleOCR engine initialized successfully")
        except ImportError as e:
            self.logger.error(f"Failed to initialize PaddleOCR engine: {e}")
            raise
    def extract_text(self, image_path:str) -> str:
        try:
            result = self.ocr.ocr(image_path, cls=True)
            text = ' '.join([line[1][0] for line in result[0] if line[1][1] > self.config.get("confidence_threshold", 0.7)])
            self.logger.info(f"Extracted {len(text)} characters from {image_path}")
            return text
        except Exception as e:
            self.logger.error(f"OCR extraction failed: {e}")
            raise
    def extract_text_with_confidence(self, image_path:str) -> List[TextResult]:
        try:
            result = self.ocr.ocr(image_path, cls=True)
            text_results = []
            for line in result[0]:
                text, confidence = line[1]
                bbox = line[0] # [[x1,y1], [x2,y2], [x3,y3], [x4,y4]]
                if confidence > self.config.get("confidence_threshold", 0.7):
                    text_results.append(TextResult(
                        text=text,
                        confidence=confidence,
                        bbox=[bbox[0][0], bbox[0][1], bbox[2][0], bbox[2][1]],
                        language=self.config.get("language", "ar")
                    ))
            return text_results
        except Exception as e:
            self.logger.error(f"OCR extraction with confidence failed: {e}")
            raise
    def is_available(self, image_path:str) -> bool:
        try:
            self.ocr.ocr(image_path, cls=True)
            return True
        except Exception as e:
            self.logger.error(f"Failed to extract text from image: {e}")
            return False