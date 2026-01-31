"""Azure Speech TTS - Voz no estilo Clipchamp (Microsoft)."""

import os
from typing import Optional

# Azure Speech usa a mesma tecnologia que Clipchamp
# Requer: pip install azure-cognitiveservices-speech


def _check_azure_available() -> bool:
    """Check if Azure Speech SDK is available."""
    try:
        import azure.cognitiveservices.speech as speechsdk
        return True
    except ImportError:
        return False


class AzureTextToSpeech:
    """Text-to-Speech using Azure Speech Services (Clipchamp-quality)."""

    def __init__(
        self,
        output_dir: str = "outputs",
        voice: str = "pt-BR-FranciscaNeural",
        subscription_key: Optional[str] = None,
        region: Optional[str] = None
    ):
        """Initialize Azure TTS.

        Args:
            output_dir: Directory to save audio
            voice: Voice name (pt-BR-FranciscaNeural, pt-BR-AntonioNeural, etc.)
            subscription_key: Azure Speech key (or env AZURE_SPEECH_KEY)
            region: Azure region (or env AZURE_SPEECH_REGION, e.g. brazilsouth)
        """
        self.output_dir = output_dir
        self.voice = voice
        self.subscription_key = subscription_key or os.getenv("AZURE_SPEECH_KEY")
        self.region = region or os.getenv("AZURE_SPEECH_REGION", "brazilsouth")
        os.makedirs(output_dir, exist_ok=True)

    def generate_audio(
        self,
        text: str,
        output_filename: Optional[str] = None,
        **kwargs
    ) -> str:
        """Generate audio using Azure Speech."""
        if not _check_azure_available():
            raise ImportError("Install: pip install azure-cognitiveservices-speech")
        if not self.subscription_key:
            raise ValueError("Set AZURE_SPEECH_KEY in config/api_keys.env")

        import azure.cognitiveservices.speech as speechsdk

        if output_filename is None:
            import hashlib
            output_filename = f"tts_azure_{hashlib.md5(text.encode()).hexdigest()}.mp3"
        output_path = os.path.join(self.output_dir, output_filename)

        speech_config = speechsdk.SpeechConfig(
            subscription=self.subscription_key,
            region=self.region
        )
        speech_config.speech_synthesis_voice_name = self.voice
        audio_config = speechsdk.audio.AudioOutputConfig(filename=output_path)
        synthesizer = speechsdk.SpeechSynthesizer(
            speech_config=speech_config,
            audio_config=audio_config
        )
        result = synthesizer.speak_text_async(text).get()
        if result.reason != speechsdk.ResultReason.SynthesizingAudioCompleted:
            raise RuntimeError(f"Azure TTS failed: {result.reason}")
        return output_path
