import io
import logging
import os
import yaml
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    MessageHandler,
    CommandHandler,
    filters,
)

from .llm import LLMClient
from .voice import VoiceClient
from .upsell import UpsellManager


logging.basicConfig(level=logging.INFO)

CONFIG_PATH = os.environ.get("BOT_CONFIG", "config.yaml")
with open(CONFIG_PATH) as fh:
    CONFIG = yaml.safe_load(fh)

llm_client = LLMClient(os.environ.get("OPENAI_API_KEY", ""), CONFIG.get("llm_model", "gpt-3.5-turbo"))
voice_client = VoiceClient(os.environ.get("ELEVEN_API_KEY", ""), CONFIG.get("voice_id", ""))
upsell = UpsellManager(CONFIG.get("free_message_limit", 3))


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(CONFIG.get("welcome_message", "Salut!"))


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id
    text = update.message.text
    upsell.record_message(user_id)

    history = context.user_data.setdefault("history", [])
    history.append({"role": "user", "content": text})
    reply = llm_client.generate_reply(history)
    history.append({"role": "assistant", "content": reply})
    await update.message.reply_text(reply)

    if upsell.needs_voice_offer(user_id):
        audio = voice_client.synthesize(reply)
        bio = io.BytesIO(audio)
        bio.name = "voice.mp3"
        await update.message.reply_voice(voice=bio)
        upsell.record_voice_sent(user_id)
        await update.message.reply_text(CONFIG.get("voice_upsell", """Pour aller plus loin, clique ici: {link}""").format(link=CONFIG.get("ppv_link", "")))
    elif upsell.needs_video_offer(user_id):
        upsell.record_video_offered(user_id)
        await update.message.reply_text(CONFIG.get("video_upsell", """Envie d'une vidéo? {link}""").format(link=CONFIG.get("video_link", "")))


def main() -> None:
    token = os.environ["TELEGRAM_BOT_TOKEN"]
    app = ApplicationBuilder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    app.run_polling()


if __name__ == "__main__":
    main()
