import asyncio
from types import SimpleNamespace
from telegram import Update
from telegram.ext import Application, CallbackContext

from bot.main import handle_message, llm_client, voice_client, upsell, CONFIG


class DummyMessage:
    def __init__(self, text, user_id):
        self.text = text
        self.from_user = SimpleNamespace(id=user_id)
        self.texts = []
        self.voices = []

    async def reply_text(self, text, **kwargs):
        self.texts.append(text)

    async def reply_voice(self, voice, **kwargs):
        self.voices.append(voice)


def build_context(user_id):
    app = Application.builder().token("TEST").build()
    return CallbackContext(application=app, chat_id=user_id, user_id=user_id)


def test_handle_message_text_only(monkeypatch):
    message = DummyMessage("Bonjour", 42)
    update = Update(update_id=1, message=message)
    context = build_context(42)

    monkeypatch.setattr(llm_client, "generate_reply", lambda history: "Salut" )
    monkeypatch.setattr(upsell, "record_message", lambda uid: None)
    monkeypatch.setattr(upsell, "needs_voice_offer", lambda uid: False)
    monkeypatch.setattr(upsell, "needs_video_offer", lambda uid: False)

    asyncio.run(handle_message(update, context))

    assert message.texts == ["Salut"]
    assert message.voices == []
    assert context.user_data["history"] == [
        {"role": "user", "content": "Bonjour"},
        {"role": "assistant", "content": "Salut"},
    ]


def test_handle_message_with_voice(monkeypatch):
    message = DummyMessage("Bonjour", 1)
    update = Update(update_id=2, message=message)
    context = build_context(1)

    monkeypatch.setattr(llm_client, "generate_reply", lambda history: "Salut" )
    synth_calls = []

    def fake_synthesize(text):
        synth_calls.append(text)
        return b"data"

    monkeypatch.setattr(voice_client, "synthesize", fake_synthesize)
    monkeypatch.setattr(upsell, "record_message", lambda uid: None)
    monkeypatch.setattr(upsell, "needs_voice_offer", lambda uid: True)
    monkeypatch.setattr(upsell, "needs_video_offer", lambda uid: False)
    monkeypatch.setattr(upsell, "record_voice_sent", lambda uid: None)

    asyncio.run(handle_message(update, context))

    assert message.texts[0] == "Salut"
    assert message.texts[1] == CONFIG["voice_upsell"].format(link=CONFIG["ppv_link"])
    assert len(message.voices) == 1
    assert synth_calls == ["Salut"]
