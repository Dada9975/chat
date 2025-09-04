import types
import openai
import requests
from bot.llm import LLMClient
from bot.voice import VoiceClient


def test_llm_client_generates_reply(monkeypatch):
    calls = {}

    def fake_create(*, model, messages):
        calls["model"] = model
        calls["messages"] = messages
        return {"choices": [{"message": {"content": "Bonjour"}}]}

    monkeypatch.setattr(openai.ChatCompletion, "create", fake_create)

    client = LLMClient(api_key="test", model="test-model")
    conv = [{"role": "user", "content": "Salut"}]
    reply = client.generate_reply(conv)

    assert reply == "Bonjour"
    assert calls["model"] == "test-model"
    assert calls["messages"] == conv


class DummyResponse:
    def __init__(self, content=b"audio"):
        self.content = content

    def raise_for_status(self):
        pass


def test_voice_client_synthesize(monkeypatch):
    api_key = "key"
    voice_id = "voice123"

    def fake_post(url, json, headers):
        assert url == f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
        assert json == {"text": "Hello"}
        assert headers["xi-api-key"] == api_key
        return DummyResponse(b"data")

    monkeypatch.setattr(requests, "post", fake_post)

    client = VoiceClient(api_key, voice_id)
    result = client.synthesize("Hello")

    assert result == b"data"
