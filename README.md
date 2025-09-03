# OnlyFans Telegram Bot

Prototype de bot Telegram pour automatiser les conversations et l'upsell sur OnlyFans.

## Fonctionnalités
- Réponses automatiques via un LLM (OpenAI).
- Génération de messages vocaux avec ElevenLabs.
- Logique d'upsell : après quelques messages, envoi d'un vocal puis proposition de contenu vidéo via un lien PPV.
- Configuration simple via `config.yaml`.

## Installation
```bash
pip install -r requirements.txt
```

## Variables d'environnement
- `TELEGRAM_BOT_TOKEN`
- `OPENAI_API_KEY`
- `ELEVEN_API_KEY`

## Lancement
```bash
python -m bot.main
```

## Tests
```bash
pytest
```
