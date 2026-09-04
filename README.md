# moodiji.

A silly AI Emoji Translator website built with Python + Flask.

## Features

- Moodiji logo and comic-book aesthetic
- Emoji sentence translator
- Copy button
- Regenerate button
- Local browser history
- Deliberately useless score
- Responsive mobile layout

## Run

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
python app.py
```

Then open http://127.0.0.1:5000

## Make it genuinely AI-powered

The current translator is intentionally local and doesn't need an API key. To make it truly AI-powered, replace `translate()` in `app.py` with a call to the AI provider/API you choose, while keeping the same `/translate` JSON response format.
