import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
from utils.config import load_config

if __name__ == "__main__":
    config = load_config(r"configs\tts\gtts.yaml")
    print(config)