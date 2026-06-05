# Study Buddy v0.2.0-BETA

A quiz tool + AI-powered Anki flashcard generator.
Works on Windows, Linux, and macOS.

---

## Setup

```bash
pip install -r requirements.txt
python study_buddy.py
```

---

## Features

**Quiz Mode**
- Load your own question banks (JSON or CSV)
- Filter by topic, set question count, shuffle
- Self-grade each card with live score tracking

**Flashcard Generator**
- Paste notes and/or load a question bank
- AI generates Anki-compatible flashcards
- Export as `.apkg` (direct Anki import), `.csv`, or `.txt`

**Settings**
- Groq — free tier at console.groq.com
- OpenRouter — keys at openrouter.ai/keys
- Settings saved to `~/.studybuddy_config.json`

---

## Question Bank Format

JSON (list):
```json
[
  {"question": "What is the powerhouse of the cell?", "answer": "Mitochondria", "topic": "Biology"},
  {"question": "What is Newton's 2nd law?", "answer": "F = ma", "topic": "Physics"}
]
```

JSON (dict by topic):
```json
{
  "Biology": [
    {"question": "What is the powerhouse of the cell?", "answer": "Mitochondria"}
  ]
}
```

CSV:
```
question,answer,topic
What is the powerhouse of the cell?,Mitochondria,Biology
```

Column aliases: `question` / `q` / `front` — `answer` / `a` / `back` — `topic` / `category` / `deck`

---

## Packaging

```bash
pip install pyinstaller

# Windows
pyinstaller --windowed --onefile --name "Study Buddy" study_buddy.py

# macOS
pyinstaller --windowed --onefile --name "Study Buddy" study_buddy.py

# Linux
pyinstaller --onefile --name "study-buddy" study_buddy.py
```

---

## Changelog

### v0.2.0-BETA
- Full PyQt6 GUI rewrite
- AI flashcard generation via Groq and OpenRouter
- Anki `.apkg` export
- Custom question bank loading (JSON + CSV)
- macOS support

### v0.1.1-BETA
- Terminal-based quiz app
- Windows and Linux only
