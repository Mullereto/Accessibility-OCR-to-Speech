from abc import ABC, abstractmethod
from typing import List, Dict, Any
from dataclasses import dataclass


@dataclass
class TextResult:
    text: str
    confidence: float = 0.0

    bbox: List[int] = None # [x1, y1, x2, y2]

    language: str = 'ar'
    
class BaseOCREngine(ABC):
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
    @abstractmethod
    def extract_text(self, image_path:str) -> str:
        """Extract text from image, return plain text."""
        pass
    @abstractmethod
    def extract_text_with_confidence(self, image_path:str) -> List[TextResult]:
        """Extract text from image, return text with confidence."""
        pass

    def is_available(self) -> bool:
        """Check if the engine is available and ready to use."""
        return True
    
