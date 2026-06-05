# Study Buddy v0.2.0-BETA

Study Buddy helps you quiz yourself and generate Anki flashcards using AI.
It runs on Windows, Linux, and macOS — pick whichever works for you below.

---

## Download & Run

### Windows
1. Download `Study.Buddy.exe` from the [Releases](../../releases) page
2. Double-click it — no installation needed

### macOS
1. Download `Study.Buddy.app` from the [Releases](../../releases) page
2. Drag it into your Applications folder
3. Right-click → Open the first time (macOS will ask you to confirm)

### Linux
1. Download `study-buddy` from the [Releases](../../releases) page
2. Run the setup below to add it to your desktop

```bash
# Make it executable
chmod +x study-buddy

# Create a launcher on your desktop
cat > ~/Desktop/study-buddy.desktop << 'DESKTOP'
[Desktop Entry]
Type=Application
Name=Study Buddy
Exec=/path/to/study-buddy
Icon=study-buddy
Terminal=false
Categories=Education;
DESKTOP

# Make the launcher executable
chmod +x ~/Desktop/study-buddy.desktop
```

> Replace `/path/to/study-buddy` with the actual path where you saved the file,
> for example `/home/yourname/Downloads/study-buddy`

---

## Features

**Quiz Mode**
Load your own question bank and get quizzed. Pick topics, set how many
questions you want, and self-grade each one. Your score is tracked as you go.

**Flashcard Generator**
Paste your notes, load a question bank, or both — then let the AI generate
Anki-ready flashcards for you. Export them as `.apkg` to import straight into
Anki, or as `.csv` / `.txt` if you prefer.

**Settings**
Connect your Groq or OpenRouter API key to power the flashcard generator.
Both have free tiers to get started. Your key is saved locally and never shared.
- Groq → [console.groq.com](https://console.groq.com)
- OpenRouter → [openrouter.ai/keys](https://openrouter.ai/keys)

---

## Question Bank Format

Study Buddy accepts JSON or CSV files. Here are the supported formats:

**JSON (list):**
```json
[
  {"question": "What is the powerhouse of the cell?", "answer": "Mitochondria", "topic": "Biology"},
  {"question": "What is Newton's 2nd law?", "answer": "F = ma", "topic": "Physics"}
]
```

**JSON (by topic):**
```json
{
  "Biology": [
    {"question": "What is the powerhouse of the cell?", "answer": "Mitochondria"}
  ]
}
```

**CSV:**
```
question,answer,topic
What is the powerhouse of the cell?,Mitochondria,Biology
What is Newton's 2nd law?,F = ma,Physics
```

Column names are flexible — `question`, `q`, or `front` all work, same with
`answer`, `a`, or `back`, and `topic`, `category`, or `deck`.

---

## Running from Source

If you'd rather run the Python source directly:

```bash
pip install -r requirements.txt
python study_buddy.py
```

Requires Python 3.11+.

---

## Changelog

### v0.2.0-BETA
- Full PyQt6 GUI — no more terminal
- AI flashcard generation via Groq and OpenRouter
- Anki `.apkg` export
- Bring your own question bank (JSON + CSV)
- macOS support added

### v0.1.1-BETA
- Terminal-based quiz app
- Windows and Linux only
