import requests


class VoiceClient:
    """Generate speech audio via ElevenLabs API."""

    def __init__(self, api_key: str, voice_id: str):
        self.api_key = api_key
        self.voice_id = voice_id

    def synthesize(self, text: str) -> bytes:
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{self.voice_id}"
        headers = {"xi-api-key": self.api_key, "Content-Type": "application/json"}
        payload = {"text": text}
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.content
