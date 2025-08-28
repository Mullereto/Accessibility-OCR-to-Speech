import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
# src/pipeline/main_pipeline.py
import logging
import json
import time
import os
from typing import Dict, Any, List
from pathlib import Path
from dataclasses import dataclass

# Use absolute imports instead of relative imports
from preprocessing.document_loader import DocumentLoader
from ocr.paddle_ocr import PaddleOCREngine
from ocr.mistral_ocr import ocr_mistral

from tts.gtts_engine import GTTSEngine
import shutil

@dataclass
class PipelineResult:
    input_path: str
    output_audio: str
    extracted_text: str
    confidence: float
    processing_time: float
    errors: List[str]
    
logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    )

class AccessibilityPipeline:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Initialize using your existing classes
        self.logger.info("Initializing pipeline components...")
        
        try:
            # Initialize document loader
            self.doc_loader = DocumentLoader()
            self.logger.info("✅ Document loader initialized successfully")
            if self.config.get('ocr') == "paddle":

                # Initialize OCR engine using your PaddleOCR class
                self.ocr_engine = PaddleOCREngine(config.get('paddle_ocr', {}))
                self.logger.info("✅ PaddleOCR engine initialized successfully")
            
            elif config.get('ocr') == "mistral":

                # Initialize OCR engine using your mistral_ocr class
                self.ocr_engine = ocr_mistral(config.get('mistral_ocr', {}))
                self.logger.info("✅ mistral_ocr engine initialized successfully")
            
            # Initialize TTS engine using your gTTS class
            self.tts_engine = GTTSEngine(config.get('gtts_tts', {}))
            self.logger.info("✅ gTTS engine initialized successfully")
            
        except Exception as e:
            self.logger.error(f"❌ Failed to initialize pipeline: {e}")
            raise
        
        self.logger.info("🎉 Pipeline initialization completed!")
    
    def process_document(self, input_path: str, output_dir: str) -> PipelineResult:
        """
        Main pipeline: Document → OCR → TTS → Audio + JSON
        Using your existing DocumentLoader, PaddleOCR, and gTTS classes
        """
        start_time = time.time()
        errors = []
        
        try:
            self.logger.info(f"🚀 Starting document processing: {input_path}")
            
            # 1. Load document using your DocumentLoader class
            self.logger.info("📄 Step 1: Loading document...")
            image_paths = self.doc_loader.load_document(input_path)

            self.logger.info(f"✅ Loaded {len(image_paths)} pages/images")
            
            # 2. Extract text from all pages using your PaddleOCR class
            self.logger.info("🔍 Step 2: Extracting text with PaddleOCR...")
            all_text = []
            all_text_results = []
            successful_pages = 0
            
            for i, img_path in enumerate(image_paths):
                try:
                    self.logger.info(f"Processing page/image {i+1}/{len(image_paths)}: {img_path}")
                    if self.config.get('ocr') == "paddle":

                        # Use your PaddleOCR class to extract text with confidence
                        text_results = self.ocr_engine.extract_text_with_confidence(img_path)
                        
                        if text_results:
                            # Combine all text from this page
                            page_text = ' '.join([tr.text for tr in text_results])
                            all_text.append(page_text)
                            all_text_results.extend(text_results)
                            successful_pages += 1
                            
                            self.logger.info(f"   ✅ Page {i+1}: Extracted {len(page_text)} characters")
                            self.logger.info(f"   📊 Confidence range: {min([tr.confidence for tr in text_results]):.3f} - {max([tr.confidence for tr in text_results]):.3f}")
                        else:
                            self.logger.warning(f"   ⚠️  Page {i+1}: No text extracted")
                    elif self.config.get('ocr') == "mistral":
                        # Use your mistral_ocr class to extract text
                        print("I am UP here")
                        text_results = self.ocr_engine.extract_text(img_path)
                        print("I am down here")
                        if text_results:
                            page_text = ' '.join([tr.text for tr in text_results])
                            all_text.append(page_text)
                            all_text_results.extend(text_results)
                            successful_pages += 1
                            self.logger.info(f"   ✅ Page {i+1}: Extracted {len(all_text)} characters")
                        else:
                            self.logger.warning(f"   ⚠️  Page {i+1}: No text extracted")

                except Exception as e:
                    error_msg = f"OCR failed for page {i+1} ({img_path}): {e}"
                    self.logger.error(f"❌ {error_msg}")
                    errors.append(error_msg)
            
            # Combine all extracted text
            full_text = ' '.join(all_text)
            
            if not full_text.strip():
                raise ValueError("No text was extracted from the document")
            
            # Calculate average confidence from all text results
            avg_confidence = sum([tr.confidence for tr in all_text_results]) / len(all_text_results) if all_text_results else 0
            
            self.logger.info(f"📝 OCR Summary: {len(full_text)} total characters, {successful_pages} pages successful")
            self.logger.info(f"📊 Overall confidence: {avg_confidence:.3f}")
            
            # 3. Generate speech using your gTTS class
            self.logger.info("🔊 Step 3: Generating speech with gTTS...")
            
            # Create output directory if it doesn't exist
            os.makedirs(output_dir, exist_ok=True)
            
            # Generate output filenames
            base_name = Path(input_path).stem
            output_audio = os.path.join(output_dir, f"{base_name}_audio.mp3")
            
            # Synthesize speech using your gTTS class
            audio_result = self.tts_engine.synthesize(full_text, output_audio)
            self.logger.info(f"✅ Speech synthesis completed: {output_audio}")
            
            # 4. Save results as JSON
            self.logger.info("💾 Step 4: Saving results...")
            json_output = os.path.join(output_dir, f"{base_name}_results.json")
            
            results = {
                "input_path": input_path,
                "output_audio": output_audio,
                "extracted_text": full_text,
                "confidence": round(avg_confidence, 3),
                "processing_time": round(time.time() - start_time, 2),
                "pages_processed": len(image_paths),
                "successful_pages": successful_pages,
                "errors": errors,
                "ocr_engine": self.config.get('ocr'),
                "tts_engine": "gtts",
                "audio_metadata": {
                    "duration": audio_result.duration,
                    "sample_rate": audio_result.sample_rate,
                    "language": audio_result.language,
                    "text_length": audio_result.text_length
                },
                "text_details": [
                    {
                        "text": tr.text,
                        "confidence": tr.confidence,
                        "bbox": tr.bbox,
                        "language": tr.language
                    } for tr in all_text_results
                ]
            }
            
            # Save JSON with proper encoding for Arabic text
            with open(json_output, 'w', encoding='utf-8') as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
            
            self.logger.info(f"✅ Results saved to: {json_output}")
            
            # 5. Return results
            processing_time = time.time() - start_time
            self.logger.info(f"🎉 Pipeline completed in {processing_time:.2f} seconds!")
            self.cleanup_temp_files()
            if input_path.endswith(".docx"):
                os.remove(input_path.replace(".docx", ".pdf"))
            return PipelineResult(
                input_path=input_path,
                output_audio=output_audio,
                extracted_text=full_text,
                confidence=avg_confidence,
                processing_time=processing_time,
                errors=errors
            )

            
        except Exception as e:
            error_msg = f"Pipeline processing failed: {e}"
            self.logger.error(f"❌ {error_msg}")
            errors.append(error_msg)
            
            # Return error results
            processing_time = time.time() - start_time
            return PipelineResult(
                input_path=input_path,
                output_audio="",
                extracted_text="",
                confidence=0,
                processing_time=processing_time,
                errors=errors
            )
        finally:
            # Always clean up temp files, whether processing succeeds or fails
            self.logger.info("🧹 Cleaning up temporary files...")
            self.cleanup_temp_files()
    
    def cleanup_temp_files(self):
        """Clean up temporary image files created during processing."""
        try:
            import shutil
            if os.path.exists("temp"):
                shutil.rmtree("temp")
                self.logger.info("🧹 Temporary files cleaned up")

        except Exception as e:
            self.logger.warning(f"Failed to cleanup temp files: {e}")


    

