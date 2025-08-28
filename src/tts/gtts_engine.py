import logging
import re
import io
from gtts import gTTS
from .base_tts import BaseTTSEngine, AudioResult
from typing import Dict, Any
from pydub import AudioSegment

class GTTSEngine(BaseTTSEngine):
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.logger = logging.getLogger(__name__)

    def synthesize(self, text: str, output_path: str) -> AudioResult:
        try:
            audio_segments = []
            lines = text.split("\n")
            self.logger.info(f"Starting TTS synthesis for {len(text)} characters")

            for line in lines:
                if not line.strip():
                    continue  # skip empty lines

                # Detect heading (starts with one or more #)
                if re.match(r"^#+", line.strip()):
                    clean_text = line.strip("# ").upper()
                    tts = gTTS(text=clean_text, lang=self.config.get("language", "ar"), slow=True)
                else:
                    tts = gTTS(text=line.strip(), lang=self.config.get("language", "ar"), slow=False)

                # Save gTTS output to memory (not file)
                mp3_fp = io.BytesIO()
                tts.write_to_fp(mp3_fp)
                mp3_fp.seek(0)

                # Load directly into AudioSegment
                audio_segments.append(AudioSegment.from_file(mp3_fp, format="mp3"))

            if not audio_segments:
                raise ValueError("No audio generated (empty text input?)")

            # Combine all segments with pause
            final_audio = audio_segments[0]
            for seg in audio_segments[1:]:
                final_audio += AudioSegment.silent(duration=600) + seg

            # Export final audio once
            final_audio.export(output_path, format="mp3")
            self.logger.info(f"TTS synthesis completed: {output_path}")

            # Estimate audio duration
            duration = len(final_audio) / 1000.0  # milliseconds → seconds
            sample_rate = self.config.get("sample_rate", 22050)

            return AudioResult(
                audio_path=output_path,
                duration=duration,
                sample_rate=sample_rate,
                language=self.config.get("language", "ar"),
                text_length=len(text),
            )

        except Exception as e:
            self.logger.error(f"TTS synthesis failed: {e}")
            raise
