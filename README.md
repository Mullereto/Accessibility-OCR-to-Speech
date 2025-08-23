# Accessibility OCR to Speech

A comprehensive system that converts documents (PDFs, images) to speech using multiple OCR engines and text-to-speech technologies, designed for accessibility and multi-language support.

## 🚀 Features

- **Multi-Engine OCR**: Support for PaddleOCR, Surya OCR, and Tesseract
- **Layout Detection**: Automatic detection of columns, tables, and document regions
- **Multi-Language TTS**: Support for multiple text-to-speech engines
- **Document Preprocessing**: Denoising, rotation correction, and normalization
- **Structured Output**: Convert OCR results to structured JSON/XML formats
- **Experiment Tracking**: MLflow integration for model training and evaluation

## 📁 Project Structure

```
accessibility-ocr-speech/
│── data/                       # Sample input PDFs/images, test files
│── docs/                       # Documentation, diagrams, research notes
│── experiments/                # MLflow logs, model training experiments
│
├── src/                        # Main source code
│   ├── preprocessing/           # Denoising, rotation, normalization
│   ├── layout/                  # Layout detection (columns, tables, regions)
│   ├── ocr/                     # OCR engines + factory
│   ├── structure/               # Map OCR → structured JSON/XML
│   ├── tts/                     # Text-to-speech engines
│   ├── pipeline/                # End-to-end pipeline
│   └── utils/                   # Helpers (logging, config, language detection)
│
├── tests/                       # Unit/integration tests
├── requirements.txt             # Dependencies
└── run_demo.py                  # Quick demo entry point
```

## 🛠️ Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd accessibility-ocr-speech
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Install additional system dependencies:
   - **Tesseract**: Follow [installation guide](https://github.com/tesseract-ocr/tesseract)
   - **PaddlePaddle**: Follow [installation guide](https://www.paddlepaddle.org.cn/install/quick)

## 🚀 Quick Start

Run the demo script to test the system:

```bash
python run_demo.py --input data/sample.pdf --output output/audio.mp3
```

## 🔧 Configuration

Create a `.env` file in the root directory:

```env
# OCR Settings
OCR_ENGINE=paddle  # paddle, surya, tesseract
OCR_CONFIDENCE_THRESHOLD=0.7

# TTS Settings
TTS_ENGINE=gtts  # gtts, coqui, openai
OPENAI_API_KEY=your_api_key_here

# Logging
LOG_LEVEL=INFO
```

## 📚 Usage Examples

### Basic OCR to Speech Pipeline

```python
from src.pipeline.main_pipeline import AccessibilityPipeline

pipeline = AccessibilityPipeline()
result = pipeline.process_document(
    input_path="document.pdf",
    output_path="output.mp3",
    language="en"
)
```

### Using Specific OCR Engine

```python
from src.ocr.ocr_factory import OCRFactory

ocr = OCRFactory.create_engine("paddle")
text = ocr.extract_text("image.jpg")
```

### Custom TTS Engine

```python
from src.tts.coqui_engine import CoquiTTSEngine

tts = CoquiTTSEngine()
audio = tts.synthesize("Hello, world!", "en")
```

## 🧪 Testing

Run the test suite:

```bash
pytest tests/ -v
```

Run with coverage:

```bash
pytest tests/ --cov=src --cov-report=html
```

## 📊 Experiment Tracking

The project integrates with MLflow for experiment tracking:

```bash
mlflow ui
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- PaddleOCR team for the excellent OCR engine
- Coqui AI for the TTS framework
- Tesseract community for the open-source OCR solution
- All contributors and researchers in the accessibility field

## 📞 Support

For questions and support, please open an issue on GitHub or contact the development team.
