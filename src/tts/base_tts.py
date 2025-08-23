from abc import ABC, abstractmethod
from typing import Dict, Any
from dataclasses import dataclass

@dataclass
class AudioResult:
    audio_path: str
    duration: float
    sample_rate: int
    language: str
    text_length: int


class BaseTTSEngine(ABC):
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
    @abstractmethod
    def synthesize(self, text: str, language: str) -> AudioResult:
        """Convert text to speech and save to file."""
        pass
    
    def is_available(self) -> bool:
        """Check if the engine is available and ready to use."""
        return True