from mistralai import Mistral
from mistralai.models import ImageURLChunk  # important import
from .base_ocr import TextResult
import cv2, base64
from typing import List

class ocr_mistral:
    def __init__(self, config):
        self.api_key = config["api_key"]
        self.client = Mistral(api_key=self.api_key)
    def extract_text(self, img_path) -> List[TextResult]:
        b64_prefixed = f"data:image/png;base64,{img_path}"
        
        # Call API
        ocr_response = self.client.ocr.process(
        model="mistral-ocr-latest",
        document=ImageURLChunk(image_url=b64_prefixed),
        include_image_base64=False
        )
        text_results = []
        
        for res in ocr_response.pages:
            text_results.append(TextResult(text=res.markdown))
        return text_results
