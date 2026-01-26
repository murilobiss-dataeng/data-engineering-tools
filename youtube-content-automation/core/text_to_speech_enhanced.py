"""Enhanced Text-to-Speech with better quality for YouTube."""

import os
import asyncio
import edge_tts
from typing import Optional
from pydub import AudioSegment


class EnhancedTextToSpeech:
    """Generate high-quality speech audio using edge-tts."""
    
    # Brazilian Portuguese voices available in edge-tts
    BRAZILIAN_VOICES = [
        "pt-BR-FranciscaNeural",  # Female, natural
        "pt-BR-AntonioNeural",     # Male, natural
        "pt-BR-ThalitaNeural",     # Female, friendly
    ]
    
    def __init__(self, output_dir: str = "outputs", voice: str = None):
        """Initialize enhanced TTS engine.
        
        Args:
            output_dir: Directory to save audio files
            voice: Voice name (default: FranciscaNeural for female)
        """
        self.output_dir = output_dir
        self.voice = voice or self.BRAZILIAN_VOICES[0]  # FranciscaNeural
        os.makedirs(output_dir, exist_ok=True)
    
    async def _generate_audio_async(
        self,
        text: str,
        output_path: str,
        rate: str = "+0%",
        pitch: str = "+0Hz"
    ) -> str:
        """Generate audio asynchronously.
        
        Args:
            text: Text to convert
            output_path: Output file path
            rate: Speech rate (e.g., "+0%", "+10%", "-10%")
            pitch: Pitch adjustment
            
        Returns:
            Path to generated audio
        """
        communicate = edge_tts.Communicate(
            text=text,
            voice=self.voice,
            rate=rate,
            pitch=pitch
        )
        await communicate.save(output_path)
        return output_path
    
    def generate_audio(
        self,
        text: str,
        output_filename: Optional[str] = None,
        rate: str = "+0%",
        pitch: str = "+0Hz"
    ) -> str:
        """Generate audio file from text.
        
        Args:
            text: Text to convert to speech
            output_filename: Optional output filename
            rate: Speech rate adjustment
            pitch: Pitch adjustment
            
        Returns:
            Path to generated audio file
        """
        if output_filename is None:
            import hashlib
            text_hash = hashlib.md5(text.encode()).hexdigest()
            output_filename = f"tts_enhanced_{text_hash}.mp3"
        
        output_path = os.path.join(self.output_dir, output_filename)
        
        # Run async function
        asyncio.run(self._generate_audio_async(text, output_path, rate, pitch))
        
        return output_path
    
    def generate_audio_with_pauses(
        self,
        text: str,
        output_filename: Optional[str] = None,
        pause_duration: float = 0.6
    ) -> str:
        """Generate audio with natural pauses between sentences.
        
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
            output_filename = f"tts_enhanced_{text_hash}.mp3"
        
        output_path = os.path.join(self.output_dir, output_filename)
        final_audio.export(output_path, format="mp3", bitrate="192k")
        
        return output_path
    
    def get_audio_duration(self, audio_path: str) -> float:
        """Get duration of audio file in seconds."""
        audio = AudioSegment.from_mp3(audio_path)
        return len(audio) / 1000.0
