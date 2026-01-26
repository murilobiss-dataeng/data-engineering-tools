"""Text-to-Speech generation for video narration."""

import os
from gtts import gTTS
from pydub import AudioSegment
from typing import Optional


class TextToSpeech:
    """Generate speech audio from text."""
    
    def __init__(self, output_dir: str = "outputs", language: str = "pt", slow: bool = False, tld: str = "com.br"):
        """Initialize TTS engine.
        
        Args:
            output_dir: Directory to save audio files
            language: Language code (default: 'pt' for Portuguese)
            slow: Whether to speak slowly (False for YouTube-quality speed)
            tld: Top-level domain for TTS (com.br for Brazilian Portuguese)
        """
        self.output_dir = output_dir
        self.language = language
        self.slow = slow
        self.tld = tld  # Use Brazilian domain for better Portuguese voice
        os.makedirs(output_dir, exist_ok=True)
    
    def generate_audio(
        self,
        text: str,
        output_filename: Optional[str] = None,
        language: Optional[str] = None
    ) -> str:
        """Generate audio file from text.
        
        Args:
            text: Text to convert to speech
            output_filename: Optional output filename
            language: Optional language override
            
        Returns:
            Path to generated audio file
        """
        if output_filename is None:
            import hashlib
            text_hash = hashlib.md5(text.encode()).hexdigest()
            output_filename = f"tts_{text_hash}.mp3"
        
        output_path = os.path.join(self.output_dir, output_filename)
        
        # Use provided language or default
        lang = language or self.language
        
        # Generate speech with Brazilian Portuguese domain for better voice quality
        # tld='com.br' gives more natural Brazilian Portuguese voice
        tts = gTTS(text=text, lang=lang, slow=self.slow, tld=self.tld)
        tts.save(output_path)
        
        return output_path
    
    def generate_audio_with_pauses(
        self,
        text: str,
        output_filename: Optional[str] = None,
        pause_duration: float = 0.5
    ) -> str:
        """Generate audio with pauses between sentences.
        
        Args:
            text: Text to convert to speech
            output_filename: Optional output filename
            pause_duration: Duration of pause in seconds
            
        Returns:
            Path to generated audio file
        """
        # Split text into sentences
        import re
        sentences = re.split(r'[.!?]\s+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        audio_segments = []
        
        for i, sentence in enumerate(sentences):
            # Generate audio for sentence
            sentence_audio = self.generate_audio(
                sentence,
                output_filename=f"temp_sentence_{i}.mp3"
            )
            
            # Load audio segment
            segment = AudioSegment.from_mp3(sentence_audio)
            audio_segments.append(segment)
            
            # Add pause (except after last sentence)
            if i < len(sentences) - 1:
                pause_ms = int(pause_duration * 1000)
                pause = AudioSegment.silent(duration=pause_ms)
                audio_segments.append(pause)
            
            # Clean up temp file
            if os.path.exists(sentence_audio):
                os.remove(sentence_audio)
        
        # Combine all segments
        if audio_segments:
            final_audio = sum(audio_segments)
        else:
            final_audio = AudioSegment.silent(duration=1000)
        
        # Save final audio
        if output_filename is None:
            import hashlib
            text_hash = hashlib.md5(text.encode()).hexdigest()
            output_filename = f"tts_{text_hash}.mp3"
        
        output_path = os.path.join(self.output_dir, output_filename)
        final_audio.export(output_path, format="mp3")
        
        return output_path
    
    def get_audio_duration(self, audio_path: str) -> float:
        """Get duration of audio file in seconds.
        
        Args:
            audio_path: Path to audio file
            
        Returns:
            Duration in seconds
        """
        audio = AudioSegment.from_mp3(audio_path)
        return len(audio) / 1000.0
