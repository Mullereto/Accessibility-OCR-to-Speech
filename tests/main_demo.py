import sys
import os

# Add src to path so we can import from src modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from pipeline.main_pipeline import AccessibilityPipeline
from utils.config import load_config

# The pipeline now uses all your existing classes!

paddle_ocr_config = load_config(r"configs\ocr\paddle.yaml")
tts_config = load_config(r"configs\tts\gtts.yaml")
mistral_config = load_config(r"configs\ocr\mistral.yaml")

config = {
    'ocr': "mistral",
    
    'mistral_ocr': mistral_config,
    
    'paddle_ocr': paddle_ocr_config,

    'gtts_tts': tts_config
}

pipeline = AccessibilityPipeline(config)
result = pipeline.process_document(r"docs\ex.pdf", r"output/")