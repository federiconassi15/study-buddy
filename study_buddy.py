"""
Study Buddy — PyQt6 GUI
Quiz mode + AI-powered Anki flashcard generator
Supports Groq and OpenRouter APIs
"""

import sys
import json
import csv
import random
import re
import hashlib
import requests
import genanki
import os
from pathlib import Path
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QTextEdit, QLineEdit, QFileDialog,
    QTabWidget, QComboBox, QProgressBar, QScrollArea, QFrame,
    QSplitter, QMessageBox, QSpinBox, QCheckBox, QStackedWidget,
    QListWidget, QListWidgetItem, QRadioButton, QButtonGroup,
    QGroupBox, QSizePolicy, QToolButton
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QTimer, QSize, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QFont, QColor, QPalette, QIcon, QFontDatabase, QPixmap, QPainter, QBrush


# ── Palette ────────────────────────────────────────────────────────────────────
BG        = "#0d0f0e"
BG2       = "#131615"
BG3       = "#1a1e1c"
BORDER    = "#2a312d"
ACCENT    = "#4ade80"        # green
ACCENT2   = "#f59e0b"        # amber
TEXT      = "#e2e8e4"
TEXT_DIM  = "#6b7a70"
TEXT_DARK = "#3a4a3f"
RED       = "#f87171"
CARD_BG   = "#161b18"


STYLESHEET = f"""
QMainWindow, QWidget {{
    background-color: {BG};
    color: {TEXT};
    font-family: 'JetBrains Mono', 'Fira Code', 'Consolas', monospace;
    font-size: 13px;
}}

QTabWidget::pane {{
    border: 1px solid {BORDER};
    background: {BG2};
    border-radius: 0px;
}}

QTabBar::tab {{
    background: {BG};
    color: {TEXT_DIM};
    padding: 10px 24px;
    border: none;
    border-bottom: 2px solid transparent;
    font-size: 12px;
    letter-spacing: 1.5px;
    text-transform: uppercase;
}}

QTabBar::tab:selected {{
    color: {ACCENT};
    border-bottom: 2px solid {ACCENT};
    background: {BG2};
}}

QTabBar::tab:hover:!selected {{
    color: {TEXT};
    background: {BG3};
}}

QPushButton {{
    background-color: transparent;
    color: {ACCENT};
    border: 1px solid {ACCENT};
    padding: 8px 20px;
    font-family: 'JetBrains Mono', 'Fira Code', 'Consolas', monospace;
    font-size: 12px;
    letter-spacing: 1px;
    border-radius: 2px;
}}

QPushButton:hover {{
    background-color: {ACCENT};
    color: {BG};
}}

QPushButton:pressed {{
    background-color: #22c55e;
}}

QPushButton:disabled {{
    color: {TEXT_DARK};
    border-color: {TEXT_DARK};
}}

QPushButton#danger {{
    color: {RED};
    border-color: {RED};
}}

QPushButton#danger:hover {{
    background-color: {RED};
    color: {BG};
}}

QPushButton#amber {{
    color: {ACCENT2};
    border-color: {ACCENT2};
}}

QPushButton#amber:hover {{
    background-color: {ACCENT2};
    color: {BG};
}}

QPushButton#correct {{
    background-color: {ACCENT};
    color: {BG};
    border-color: {ACCENT};
    font-size: 13px;
    padding: 10px 28px;
}}

QPushButton#wrong {{
    background-color: {RED};
    color: {BG};
    border-color: {RED};
    font-size: 13px;
    padding: 10px 28px;
}}

QLineEdit, QTextEdit, QSpinBox, QComboBox {{
    background-color: {BG3};
    color: {TEXT};
    border: 1px solid {BORDER};
    padding: 8px;
    font-family: 'JetBrains Mono', 'Fira Code', 'Consolas', monospace;
    font-size: 13px;
    selection-background-color: {ACCENT};
    selection-color: {BG};
    border-radius: 2px;
}}

QLineEdit:focus, QTextEdit:focus {{
    border-color: {ACCENT};
}}

QComboBox::drop-down {{
    border: none;
    padding-right: 8px;
}}

QComboBox::down-arrow {{
    color: {ACCENT};
}}

QComboBox QAbstractItemView {{
    background-color: {BG3};
    color: {TEXT};
    border: 1px solid {BORDER};
    selection-background-color: {ACCENT};
    selection-color: {BG};
}}

QScrollBar:vertical {{
    background: {BG};
    width: 6px;
    border: none;
}}

QScrollBar::handle:vertical {{
    background: {BORDER};
    border-radius: 3px;
    min-height: 20px;
}}

QScrollBar::handle:vertical:hover {{
    background: {ACCENT};
}}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0px;
}}

QProgressBar {{
    background-color: {BG3};
    border: none;
    height: 3px;
    text-align: center;
    border-radius: 1px;
}}

QProgressBar::chunk {{
    background-color: {ACCENT};
    border-radius: 1px;
}}

QFrame#card {{
    background-color: {CARD_BG};
    border: 1px solid {BORDER};
    border-radius: 2px;
}}

QFrame#separator {{
    background-color: {BORDER};
}}

QLabel#heading {{
    color: {ACCENT};
    font-size: 11px;
    letter-spacing: 2px;
    text-transform: uppercase;
}}

QLabel#dim {{
    color: {TEXT_DIM};
    font-size: 12px;
}}

QLabel#score_big {{
    color: {ACCENT};
    font-size: 36px;
    font-weight: bold;
}}

QLabel#question_text {{
    color: {TEXT};
    font-size: 16px;
    line-height: 1.6;
}}

QListWidget {{
    background-color: {BG3};
    border: 1px solid {BORDER};
    color: {TEXT};
    font-family: 'JetBrains Mono', 'Fira Code', 'Consolas', monospace;
    font-size: 12px;
    outline: none;
}}

QListWidget::item {{
    padding: 6px 10px;
    border-bottom: 1px solid {BG};
}}

QListWidget::item:selected {{
    background-color: {BG};
    color: {ACCENT};
    border-left: 2px solid {ACCENT};
}}

QListWidget::item:hover:!selected {{
    background-color: {BG};
}}

QCheckBox {{
    spacing: 8px;
}}

QCheckBox::indicator {{
    width: 14px;
    height: 14px;
    border: 1px solid {BORDER};
    background: {BG3};
    border-radius: 2px;
}}

QCheckBox::indicator:checked {{
    background: {ACCENT};
    border-color: {ACCENT};
}}

QGroupBox {{
    border: 1px solid {BORDER};
    margin-top: 16px;
    padding: 12px;
    font-size: 11px;
    letter-spacing: 1px;
    color: {TEXT_DIM};
}}

QGroupBox::title {{
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 6px;
    color: {TEXT_DIM};
    letter-spacing: 2px;
    font-size: 10px;
    text-transform: uppercase;
}}

QSpinBox::up-button, QSpinBox::down-button {{
    background: {BORDER};
    border: none;
    width: 16px;
}}
"""


# ── Helpers ────────────────────────────────────────────────────────────────────

def separator():
    line = QFrame()
    line.setObjectName("separator")
    line.setFrameShape(QFrame.Shape.HLine)
    line.setFixedHeight(1)
    return line


def label(text, obj_name=None, wrap=False):
    lbl = QLabel(text)
    if obj_name:
        lbl.setObjectName(obj_name)
    if wrap:
        lbl.setWordWrap(True)
    return lbl


def heading(text):
    lbl = QLabel(text)
    lbl.setObjectName("heading")
    return lbl


def load_question_bank(path: str) -> list[dict]:
    """Load questions from JSON or CSV. Returns list of {question, answer, topic?}"""
    path = Path(path)
    questions = []

    if path.suffix.lower() == ".json":
        raw = json.loads(path.read_text(encoding="utf-8"))
        # Support multiple formats
        if isinstance(raw, list):
            for item in raw:
                if isinstance(item, dict):
                    q = item.get("question") or item.get("q") or item.get("front") or ""
                    a = item.get("answer") or item.get("a") or item.get("back") or ""
                    t = item.get("topic") or item.get("category") or item.get("deck") or "General"
                    if q and a:
                        questions.append({"question": q, "answer": a, "topic": t})
        elif isinstance(raw, dict):
            # {topic: [{question, answer}]} or {topic: [[q,a]]}
            for topic, items in raw.items():
                if isinstance(items, list):
                    for item in items:
                        if isinstance(item, dict):
                            q = item.get("question") or item.get("q") or ""
                            a = item.get("answer") or item.get("a") or ""
                            if q and a:
                                questions.append({"question": q, "answer": a, "topic": topic})
                        elif isinstance(item, (list, tuple)) and len(item) >= 2:
                            questions.append({"question": item[0], "answer": item[1], "topic": topic})

    elif path.suffix.lower() == ".csv":
        with open(path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                keys = {k.lower(): v for k, v in row.items()}
                q = keys.get("question") or keys.get("q") or keys.get("front") or ""
                a = keys.get("answer") or keys.get("a") or keys.get("back") or ""
                t = keys.get("topic") or keys.get("category") or keys.get("deck") or "General"
                if q and a:
                    questions.append({"question": q.strip(), "answer": a.strip(), "topic": t.strip()})

    return questions


def normalize(text: str) -> str:
    return re.sub(r"[^a-z0-9 ]", "", text.lower().strip())


# ── API Worker ─────────────────────────────────────────────────────────────────

class FlashcardWorker(QThread):
    progress = pyqtSignal(str)
    finished = pyqtSignal(list)   # list of (front, back)
    error    = pyqtSignal(str)

    def __init__(self, notes: str, questions: list[dict], provider: str,
                 api_key: str, model: str, num_cards: int):
        super().__init__()
        self.notes = notes
        self.questions = questions
        self.provider = provider
        self.api_key = api_key
        self.model = model
        self.num_cards = num_cards

    def run(self):
        try:
            context_parts = []
            if self.notes.strip():
                context_parts.append(f"=== NOTES ===\n{self.notes.strip()}")
            if self.questions:
                sample = random.sample(self.questions, min(60, len(self.questions)))
                qtext = "\n".join(f"Q: {q['question']}\nA: {q['answer']}" for q in sample)
                context_parts.append(f"=== QUESTION BANK SAMPLE ===\n{qtext}")

            context = "\n\n".join(context_parts)

            prompt = f"""You are an expert study-card creator. Given the following study material, generate exactly {self.num_cards} Anki-compatible flashcards.

RULES:
- Each card: one clear, specific question on the front; concise, accurate answer on the back
- Questions must be atomic (test ONE concept)
- Vary question types: definition, explain, compare, give example, what happens when
- Do NOT copy questions verbatim from the question bank — rephrase or synthesise
- Return ONLY valid JSON, no markdown, no preamble

FORMAT:
[
  {{"front": "question text", "back": "answer text"}},
  ...
]

STUDY MATERIAL:
{context}

Generate {self.num_cards} flashcards now:"""

            self.progress.emit("Calling API…")

            if self.provider == "Groq":
                url = "https://api.groq.com/openai/v1/chat/completions"
                headers = {
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                }
            else:  # OpenRouter
                url = "https://openrouter.ai/api/v1/chat/completions"
                headers = {
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": "https://studybuddy.local",
                    "X-Title": "Study Buddy"
                }

            payload = {
                "model": self.model,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.7,
                "max_tokens": 4000,
            }

            self.progress.emit(f"Waiting for {self.provider}…")
            resp = requests.post(url, headers=headers, json=payload, timeout=60)
            resp.raise_for_status()

            content = resp.json()["choices"][0]["message"]["content"].strip()
            self.progress.emit("Parsing response…")

            # Strip markdown fences if present
            content = re.sub(r"^```[a-z]*\n?", "", content)
            content = re.sub(r"\n?```$", "", content)

            cards_raw = json.loads(content)
            cards = []
            for c in cards_raw:
                if isinstance(c, dict):
                    f = c.get("front") or c.get("question") or ""
                    b = c.get("back") or c.get("answer") or ""
                    if f and b:
                        cards.append((f.strip(), b.strip()))

            self.finished.emit(cards)

        except requests.exceptions.HTTPError as e:
            self.error.emit(f"API error {e.response.status_code}: {e.response.text[:300]}")
        except json.JSONDecodeError as e:
            self.error.emit(f"Could not parse API response as JSON.\n{e}")
        except Exception as e:
            self.error.emit(str(e))


# ── Quiz Tab ───────────────────────────────────────────────────────────────────

class QuizTab(QWidget):
    def __init__(self):
        super().__init__()
        self.all_questions = []
        self.session_questions = []
        self.current_idx = 0
        self.score = 0
        self.revealed = False
        self._build_ui()

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # ── Top bar ──
        topbar = QWidget()
        topbar.setStyleSheet(f"background:{BG2}; border-bottom: 1px solid {BORDER};")
        tb = QHBoxLayout(topbar)
        tb.setContentsMargins(20, 12, 20, 12)

        tb.addWidget(heading("QUIZ MODE"))
        tb.addStretch()

        self.lbl_bank_status = label("No bank loaded", "dim")
        tb.addWidget(self.lbl_bank_status)

        btn_load = QPushButton("LOAD BANK")
        btn_load.clicked.connect(self.load_bank)
        tb.addWidget(btn_load)

        root.addWidget(topbar)

        # ── Main splitter ──
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.setStyleSheet(f"QSplitter::handle {{ background: {BORDER}; width: 1px; }}")
        root.addWidget(splitter)

        # ─ Left: config panel ─
        left = QWidget()
        left.setMinimumWidth(220)
        left.setMaximumWidth(280)
        left.setStyleSheet(f"background:{BG2};")
        lv = QVBoxLayout(left)
        lv.setContentsMargins(16, 20, 16, 20)
        lv.setSpacing(16)

        lv.addWidget(heading("TOPICS"))
        self.topic_list = QListWidget()
        self.topic_list.setSelectionMode(QListWidget.SelectionMode.MultiSelection)
        self.topic_list.setFixedHeight(180)
        lv.addWidget(self.topic_list)

        lv.addWidget(separator())
        lv.addWidget(heading("OPTIONS"))

        n_row = QHBoxLayout()
        n_row.addWidget(label("Questions:", "dim"))
        self.spin_count = QSpinBox()
        self.spin_count.setRange(1, 999)
        self.spin_count.setValue(10)
        n_row.addWidget(self.spin_count)
        lv.addLayout(n_row)

        self.chk_shuffle = QCheckBox("Shuffle order")
        self.chk_shuffle.setChecked(True)
        lv.addWidget(self.chk_shuffle)

        lv.addStretch()

        self.btn_start = QPushButton("START QUIZ")
        self.btn_start.setEnabled(False)
        self.btn_start.clicked.connect(self.start_quiz)
        lv.addWidget(self.btn_start)

        splitter.addWidget(left)

        # ─ Right: quiz area ─
        right = QWidget()
        rv = QVBoxLayout(right)
        rv.setContentsMargins(32, 24, 32, 24)
        rv.setSpacing(0)

        self.stack = QStackedWidget()
        rv.addWidget(self.stack)

        # Page 0: empty state
        empty = QWidget()
        ev = QVBoxLayout(empty)
        ev.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_e = label("Load a question bank\nand press START QUIZ", "dim", wrap=True)
        lbl_e.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_e.setStyleSheet(f"color:{TEXT_DIM}; font-size:15px; line-height:2;")
        ev.addWidget(lbl_e)
        self.stack.addWidget(empty)

        # Page 1: quiz
        quiz_page = QWidget()
        qv = QVBoxLayout(quiz_page)
        qv.setSpacing(20)

        # Progress bar + counter
        prog_row = QHBoxLayout()
        self.lbl_counter = label("0 / 0", "dim")
        prog_row.addWidget(self.lbl_counter)
        prog_row.addStretch()
        self.lbl_score = label("Score: 0", "dim")
        prog_row.addWidget(self.lbl_score)
        qv.addLayout(prog_row)

        self.progress_bar = QProgressBar()
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setFixedHeight(3)
        qv.addWidget(self.progress_bar)

        qv.addSpacing(16)

        # Topic tag
        self.lbl_topic = label("", "heading")
        qv.addWidget(self.lbl_topic)

        # Question card
        q_card = QFrame()
        q_card.setObjectName("card")
        q_card.setMinimumHeight(140)
        qcl = QVBoxLayout(q_card)
        qcl.setContentsMargins(24, 24, 24, 24)
        self.lbl_question = QLabel("")
        self.lbl_question.setObjectName("question_text")
        self.lbl_question.setWordWrap(True)
        self.lbl_question.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.lbl_question.setStyleSheet(f"font-size: 17px; color: {TEXT}; line-height: 1.6;")
        qcl.addWidget(self.lbl_question)
        qv.addWidget(q_card)

        # Answer area (hidden until revealed)
        self.answer_frame = QFrame()
        self.answer_frame.setObjectName("card")
        self.answer_frame.setStyleSheet(f"QFrame#card {{ background: #0d1a10; border-color: {ACCENT}; }}")
        af = QVBoxLayout(self.answer_frame)
        af.setContentsMargins(24, 16, 24, 16)
        ans_head = label("ANSWER", "heading")
        af.addWidget(ans_head)
        self.lbl_answer = QLabel("")
        self.lbl_answer.setWordWrap(True)
        self.lbl_answer.setStyleSheet(f"font-size: 15px; color: {ACCENT}; margin-top: 6px;")
        af.addWidget(self.lbl_answer)
        self.answer_frame.setVisible(False)
        qv.addWidget(self.answer_frame)

        qv.addStretch()

        # Buttons row
        self.btn_reveal = QPushButton("REVEAL ANSWER  →")
        self.btn_reveal.setStyleSheet(f"""
            QPushButton {{
                background: {ACCENT}; color: {BG};
                border: none; padding: 12px 32px;
                font-size: 13px; letter-spacing: 1px;
                border-radius: 2px;
            }}
            QPushButton:hover {{ background: #22c55e; }}
        """)
        self.btn_reveal.clicked.connect(self.reveal_answer)
        qv.addWidget(self.btn_reveal, alignment=Qt.AlignmentFlag.AlignHCenter)

        grade_row = QHBoxLayout()
        grade_row.setSpacing(16)
        self.btn_wrong = QPushButton("✗  GOT IT WRONG")
        self.btn_wrong.setObjectName("danger")
        self.btn_wrong.clicked.connect(lambda: self.grade(False))
        self.btn_correct = QPushButton("✓  GOT IT RIGHT")
        self.btn_correct.setObjectName("correct")
        self.btn_correct.clicked.connect(lambda: self.grade(True))
        grade_row.addWidget(self.btn_wrong)
        grade_row.addWidget(self.btn_correct)
        self.grade_widget = QWidget()
        self.grade_widget.setLayout(grade_row)
        self.grade_widget.setVisible(False)
        qv.addWidget(self.grade_widget)

        self.stack.addWidget(quiz_page)

        # Page 2: results
        results_page = QWidget()
        resv = QVBoxLayout(results_page)
        resv.setAlignment(Qt.AlignmentFlag.AlignCenter)
        resv.setSpacing(12)

        self.lbl_result_title = label("QUIZ COMPLETE", "heading")
        self.lbl_result_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_result_title.setStyleSheet(f"color:{ACCENT}; font-size:12px; letter-spacing:4px;")
        resv.addWidget(self.lbl_result_title)

        self.lbl_result_score = label("", "score_big")
        self.lbl_result_score.setAlignment(Qt.AlignmentFlag.AlignCenter)
        resv.addWidget(self.lbl_result_score)

        self.lbl_result_pct = label("", "dim")
        self.lbl_result_pct.setAlignment(Qt.AlignmentFlag.AlignCenter)
        resv.addWidget(self.lbl_result_pct)

        resv.addSpacing(24)
        btn_restart = QPushButton("PLAY AGAIN")
        btn_restart.clicked.connect(self.start_quiz)
        resv.addWidget(btn_restart, alignment=Qt.AlignmentFlag.AlignHCenter)

        self.stack.addWidget(results_page)
        splitter.addWidget(right)
        splitter.setSizes([240, 800])

    def load_bank(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Load Question Bank", "",
            "Supported files (*.json *.csv);;JSON (*.json);;CSV (*.csv)"
        )
        if not path:
            return
        try:
            qs = load_question_bank(path)
            if not qs:
                QMessageBox.warning(self, "Empty Bank", "No valid questions found in that file.\n\nExpected columns: question, answer (and optionally topic).")
                return
            self.all_questions = qs
            topics = sorted(set(q["topic"] for q in qs))
            self.topic_list.clear()
            for t in topics:
                item = QListWidgetItem(t)
                item.setSelected(True)
                self.topic_list.addItem(item)
            self.lbl_bank_status.setText(f"{len(qs)} questions loaded")
            self.btn_start.setEnabled(True)
            self.spin_count.setMaximum(len(qs))
        except Exception as e:
            QMessageBox.critical(self, "Load Error", str(e))

    def start_quiz(self):
        selected_topics = {item.text() for item in self.topic_list.selectedItems()}
        pool = [q for q in self.all_questions if q["topic"] in selected_topics] if selected_topics else self.all_questions
        if not pool:
            QMessageBox.warning(self, "No Questions", "Select at least one topic.")
            return
        n = self.spin_count.value()
        self.session_questions = random.sample(pool, min(n, len(pool)))
        if self.chk_shuffle.isChecked():
            random.shuffle(self.session_questions)
        self.current_idx = 0
        self.score = 0
        self.progress_bar.setMaximum(len(self.session_questions))
        self.stack.setCurrentIndex(1)
        self.show_question()

    def show_question(self):
        if self.current_idx >= len(self.session_questions):
            self.show_results()
            return
        q = self.session_questions[self.current_idx]
        self.lbl_question.setText(q["question"])
        self.lbl_answer.setText(q["answer"])
        self.lbl_topic.setText(q["topic"].upper())
        self.lbl_counter.setText(f"{self.current_idx + 1} / {len(self.session_questions)}")
        self.lbl_score.setText(f"Score: {self.score}")
        self.progress_bar.setValue(self.current_idx)
        self.answer_frame.setVisible(False)
        self.btn_reveal.setVisible(True)
        self.grade_widget.setVisible(False)
        self.revealed = False

    def reveal_answer(self):
        self.answer_frame.setVisible(True)
        self.btn_reveal.setVisible(False)
        self.grade_widget.setVisible(True)
        self.revealed = True

    def grade(self, correct: bool):
        if correct:
            self.score += 1
        self.current_idx += 1
        self.show_question()

    def show_results(self):
        total = len(self.session_questions)
        pct = int(self.score / total * 100) if total else 0
        self.lbl_result_score.setText(f"{self.score} / {total}")
        self.lbl_result_pct.setText(f"{pct}%  —  {'Excellent!' if pct >= 80 else 'Keep studying!' if pct >= 50 else 'More revision needed.'}")
        self.stack.setCurrentIndex(2)


# ── Flashcard Generator Tab ────────────────────────────────────────────────────

class FlashcardTab(QWidget):
    def __init__(self, settings_ref):
        super().__init__()
        self.settings = settings_ref
        self.loaded_questions = []
        self.generated_cards = []
        self.worker = None
        self._build_ui()

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # ── Top bar ──
        topbar = QWidget()
        topbar.setStyleSheet(f"background:{BG2}; border-bottom: 1px solid {BORDER};")
        tb = QHBoxLayout(topbar)
        tb.setContentsMargins(20, 12, 20, 12)
        tb.addWidget(heading("ANKI FLASHCARD GENERATOR"))
        tb.addStretch()
        self.lbl_api_status = label("No API key set", "dim")
        tb.addWidget(self.lbl_api_status)
        root.addWidget(topbar)

        # ── Body ──
        body = QSplitter(Qt.Orientation.Horizontal)
        body.setStyleSheet(f"QSplitter::handle {{ background: {BORDER}; width: 1px; }}")
        root.addWidget(body)

        # ─ Left: inputs ─
        left = QWidget()
        left.setStyleSheet(f"background:{BG2};")
        lv = QVBoxLayout(left)
        lv.setContentsMargins(20, 20, 20, 20)
        lv.setSpacing(14)

        # Question bank section
        bank_row = QHBoxLayout()
        bank_row.addWidget(heading("QUESTION BANK  (optional)"))
        bank_row.addStretch()
        btn_load_bank = QPushButton("LOAD")
        btn_load_bank.setObjectName("amber")
        btn_load_bank.clicked.connect(self.load_bank)
        bank_row.addWidget(btn_load_bank)
        lv.addLayout(bank_row)

        self.lbl_bank = label("No bank loaded", "dim")
        lv.addWidget(self.lbl_bank)

        lv.addWidget(separator())

        # Notes section
        lv.addWidget(heading("YOUR NOTES  (paste here)"))
        self.notes_edit = QTextEdit()
        self.notes_edit.setPlaceholderText("Paste your study notes, textbook excerpts, or any text here…\n\nThe AI will use this + your question bank to generate flashcards.")
        self.notes_edit.setMinimumHeight(200)
        lv.addWidget(self.notes_edit)

        lv.addWidget(separator())

        # Config
        lv.addWidget(heading("CARD SETTINGS"))
        count_row = QHBoxLayout()
        count_row.addWidget(label("Number of cards:", "dim"))
        self.spin_cards = QSpinBox()
        self.spin_cards.setRange(1, 100)
        self.spin_cards.setValue(20)
        count_row.addWidget(self.spin_cards)
        count_row.addStretch()
        lv.addLayout(count_row)

        deck_row = QHBoxLayout()
        deck_row.addWidget(label("Deck name:", "dim"))
        self.deck_name = QLineEdit("Study Buddy")
        deck_row.addWidget(self.deck_name)
        lv.addLayout(deck_row)

        lv.addStretch()

        self.btn_generate = QPushButton("⚡  GENERATE FLASHCARDS")
        self.btn_generate.setStyleSheet(f"""
            QPushButton {{
                background: transparent; color: {ACCENT2};
                border: 1px solid {ACCENT2}; padding: 10px 24px;
                font-size: 13px; letter-spacing: 1px;
            }}
            QPushButton:hover {{ background: {ACCENT2}; color: {BG}; }}
            QPushButton:disabled {{ color: {TEXT_DARK}; border-color: {TEXT_DARK}; }}
        """)
        self.btn_generate.clicked.connect(self.generate)
        lv.addWidget(self.btn_generate)

        self.lbl_status = label("", "dim")
        self.lbl_status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lv.addWidget(self.lbl_status)

        body.addWidget(left)

        # ─ Right: preview + export ─
        right = QWidget()
        rv = QVBoxLayout(right)
        rv.setContentsMargins(20, 20, 20, 20)
        rv.setSpacing(14)

        preview_row = QHBoxLayout()
        preview_row.addWidget(heading("PREVIEW"))
        preview_row.addStretch()
        self.lbl_card_count = label("0 cards", "dim")
        preview_row.addWidget(self.lbl_card_count)
        rv.addLayout(preview_row)

        self.preview = QTextEdit()
        self.preview.setReadOnly(True)
        self.preview.setPlaceholderText("Generated flashcards will appear here…")
        self.preview.setStyleSheet(f"font-size: 12px; line-height: 1.8;")
        rv.addWidget(self.preview)

        rv.addWidget(separator())
        rv.addWidget(heading("EXPORT"))

        export_row = QHBoxLayout()
        export_row.setSpacing(10)

        self.btn_export_apkg = QPushButton("EXPORT .APKG")
        self.btn_export_apkg.setEnabled(False)
        self.btn_export_apkg.clicked.connect(self.export_apkg)
        export_row.addWidget(self.btn_export_apkg)

        self.btn_export_csv = QPushButton("EXPORT CSV")
        self.btn_export_csv.setEnabled(False)
        self.btn_export_csv.clicked.connect(self.export_csv)
        export_row.addWidget(self.btn_export_csv)

        self.btn_export_txt = QPushButton("EXPORT TXT")
        self.btn_export_txt.setEnabled(False)
        self.btn_export_txt.clicked.connect(self.export_txt)
        export_row.addWidget(self.btn_export_txt)

        rv.addLayout(export_row)

        body.addWidget(right)
        body.setSizes([420, 620])

    def update_api_status(self):
        provider = self.settings.get("provider", "Groq")
        key = self.settings.get("api_key", "")
        if key:
            self.lbl_api_status.setText(f"✓ {provider} key set")
            self.lbl_api_status.setStyleSheet(f"color: {ACCENT};")
        else:
            self.lbl_api_status.setText("No API key set — go to Settings")
            self.lbl_api_status.setStyleSheet(f"color: {ACCENT2};")

    def load_bank(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Load Question Bank", "",
            "Supported files (*.json *.csv);;JSON (*.json);;CSV (*.csv)"
        )
        if not path:
            return
        try:
            qs = load_question_bank(path)
            self.loaded_questions = qs
            self.lbl_bank.setText(f"✓  {len(qs)} questions from {Path(path).name}")
            self.lbl_bank.setStyleSheet(f"color: {ACCENT};")
        except Exception as e:
            QMessageBox.critical(self, "Load Error", str(e))

    def generate(self):
        notes = self.notes_edit.toPlainText()
        if not notes.strip() and not self.loaded_questions:
            QMessageBox.warning(self, "Nothing to use", "Add notes or load a question bank first.")
            return

        provider = self.settings.get("provider", "Groq")
        api_key = self.settings.get("api_key", "")
        model = self.settings.get("model", "")

        if not api_key:
            QMessageBox.warning(self, "API Key Missing", "Set your API key in the Settings tab.")
            return
        if not model:
            QMessageBox.warning(self, "Model Not Set", "Choose a model in the Settings tab.")
            return

        self.btn_generate.setEnabled(False)
        self.lbl_status.setText("Generating…")
        self.preview.clear()
        self.generated_cards = []

        self.worker = FlashcardWorker(
            notes=notes,
            questions=self.loaded_questions,
            provider=provider,
            api_key=api_key,
            model=model,
            num_cards=self.spin_cards.value()
        )
        self.worker.progress.connect(self.lbl_status.setText)
        self.worker.finished.connect(self.on_generated)
        self.worker.error.connect(self.on_error)
        self.worker.start()

    def on_generated(self, cards: list):
        self.generated_cards = cards
        self.btn_generate.setEnabled(True)
        self.lbl_status.setText(f"✓ {len(cards)} cards generated")
        self.lbl_status.setStyleSheet(f"color: {ACCENT};")
        self.lbl_card_count.setText(f"{len(cards)} cards")

        preview_text = ""
        for i, (front, back) in enumerate(cards, 1):
            preview_text += f"[{i}] FRONT\n{front}\n\nBACK\n{back}\n\n{'─' * 50}\n\n"
        self.preview.setPlainText(preview_text)

        for btn in [self.btn_export_apkg, self.btn_export_csv, self.btn_export_txt]:
            btn.setEnabled(True)

    def on_error(self, msg: str):
        self.btn_generate.setEnabled(True)
        self.lbl_status.setText("Error")
        self.lbl_status.setStyleSheet(f"color: {RED};")
        QMessageBox.critical(self, "Generation Failed", msg)

    def export_apkg(self):
        if not self.generated_cards:
            return
        path, _ = QFileDialog.getSaveFileName(
            self, "Export Anki Deck", f"{self.deck_name.text()}.apkg", "Anki Package (*.apkg)"
        )
        if not path:
            return
        try:
            deck_id = int(hashlib.md5(self.deck_name.text().encode()).hexdigest()[:8], 16)
            model_id = int(hashlib.md5(b"studybuddy_basic").hexdigest()[:8], 16)

            model = genanki.Model(
                model_id,
                "Study Buddy Basic",
                fields=[{"name": "Front"}, {"name": "Back"}],
                templates=[{
                    "name": "Card 1",
                    "qfmt": "{{Front}}",
                    "afmt": "{{FrontSide}}<hr id=answer>{{Back}}",
                }],
                css="""
                    .card { font-family: 'Helvetica Neue', sans-serif;
                            font-size: 18px; text-align: center;
                            color: black; background-color: white; padding: 20px; }
                    hr#answer { border-top: 1px solid #ccc; margin: 16px 0; }
                """
            )

            deck = genanki.Deck(deck_id, self.deck_name.text())
            for front, back in self.generated_cards:
                note = genanki.Note(model=model, fields=[front, back])
                deck.add_note(note)

            genanki.Package(deck).write_to_file(path)
            QMessageBox.information(self, "Exported", f"Saved {len(self.generated_cards)} cards to:\n{path}")
        except Exception as e:
            QMessageBox.critical(self, "Export Error", str(e))

    def export_csv(self):
        if not self.generated_cards:
            return
        path, _ = QFileDialog.getSaveFileName(
            self, "Export CSV", f"{self.deck_name.text()}.csv", "CSV (*.csv)"
        )
        if not path:
            return
        try:
            with open(path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["Front", "Back"])
                writer.writerows(self.generated_cards)
            QMessageBox.information(self, "Exported", f"Saved to:\n{path}")
        except Exception as e:
            QMessageBox.critical(self, "Export Error", str(e))

    def export_txt(self):
        if not self.generated_cards:
            return
        path, _ = QFileDialog.getSaveFileName(
            self, "Export TXT", f"{self.deck_name.text()}.txt", "Text (*.txt)"
        )
        if not path:
            return
        try:
            lines = []
            for front, back in self.generated_cards:
                lines.append(f"Q: {front}\nA: {back}\n")
            Path(path).write_text("\n".join(lines), encoding="utf-8")
            QMessageBox.information(self, "Exported", f"Saved to:\n{path}")
        except Exception as e:
            QMessageBox.critical(self, "Export Error", str(e))


# ── Settings Tab ───────────────────────────────────────────────────────────────

GROQ_MODELS = [
    "llama-3.3-70b-versatile",
    "llama-3.1-8b-instant",
    "mixtral-8x7b-32768",
    "gemma2-9b-it",
]

OPENROUTER_MODELS = [
    "meta-llama/llama-3.3-70b-instruct",
    "google/gemini-flash-1.5",
    "anthropic/claude-haiku",
    "mistralai/mixtral-8x7b-instruct",
    "openai/gpt-4o-mini",
    "qwen/qwen-2.5-72b-instruct",
]


class SettingsTab(QWidget):
    settings_changed = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self.config_path = Path.home() / ".studybuddy_config.json"
        self._build_ui()
        self._load_saved()

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)

        topbar = QWidget()
        topbar.setStyleSheet(f"background:{BG2}; border-bottom: 1px solid {BORDER};")
        tb = QHBoxLayout(topbar)
        tb.setContentsMargins(20, 12, 20, 12)
        tb.addWidget(heading("SETTINGS"))
        root.addWidget(topbar)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; }")
        inner = QWidget()
        inner.setStyleSheet(f"background:{BG};")
        iv = QVBoxLayout(inner)
        iv.setContentsMargins(40, 32, 40, 32)
        iv.setSpacing(24)

        # ── Provider ──
        iv.addWidget(heading("API PROVIDER"))

        prov_group = QGroupBox("Select provider")
        pg = QHBoxLayout(prov_group)
        self.btn_groq = QRadioButton("Groq")
        self.btn_openrouter = QRadioButton("OpenRouter")
        self.btn_groq.setChecked(True)
        pg.addWidget(self.btn_groq)
        pg.addWidget(self.btn_openrouter)
        pg.addStretch()
        iv.addWidget(prov_group)

        self.btn_groq.toggled.connect(self._on_provider_change)

        # ── API Key ──
        iv.addWidget(heading("API KEY"))
        key_row = QHBoxLayout()
        self.key_edit = QLineEdit()
        self.key_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.key_edit.setPlaceholderText("Paste your API key here…")
        key_row.addWidget(self.key_edit)
        self.btn_toggle = QPushButton("SHOW")
        self.btn_toggle.setFixedWidth(70)
        self.btn_toggle.clicked.connect(self._toggle_key)
        key_row.addWidget(self.btn_toggle)
        iv.addLayout(key_row)

        link_row = QHBoxLayout()
        self.lbl_link = label("Get a free Groq key at console.groq.com", "dim")
        link_row.addWidget(self.lbl_link)
        link_row.addStretch()
        iv.addLayout(link_row)

        # ── Model ──
        iv.addWidget(heading("MODEL"))
        self.model_combo = QComboBox()
        for m in GROQ_MODELS:
            self.model_combo.addItem(m)
        iv.addWidget(self.model_combo)

        self.lbl_model_note = label("Llama 3.3 70B recommended — fast and accurate for card generation.", "dim", wrap=True)
        iv.addWidget(self.lbl_model_note)

        # ── Custom model ──
        iv.addWidget(heading("CUSTOM MODEL  (optional override)"))
        self.custom_model = QLineEdit()
        self.custom_model.setPlaceholderText("e.g. google/gemini-pro (leave blank to use dropdown)")
        iv.addWidget(self.custom_model)

        iv.addWidget(separator())

        # ── Save ──
        btn_save = QPushButton("SAVE SETTINGS")
        btn_save.clicked.connect(self.save)
        iv.addWidget(btn_save, alignment=Qt.AlignmentFlag.AlignLeft)

        self.lbl_save_status = label("", "dim")
        iv.addWidget(self.lbl_save_status)

        iv.addStretch()
        scroll.setWidget(inner)
        root.addWidget(scroll)

    def _on_provider_change(self):
        is_groq = self.btn_groq.isChecked()
        self.model_combo.clear()
        if is_groq:
            for m in GROQ_MODELS:
                self.model_combo.addItem(m)
            self.lbl_link.setText("Get a free Groq key at console.groq.com")
        else:
            for m in OPENROUTER_MODELS:
                self.model_combo.addItem(m)
            self.lbl_link.setText("Get an OpenRouter key at openrouter.ai/keys")

    def _toggle_key(self):
        if self.key_edit.echoMode() == QLineEdit.EchoMode.Password:
            self.key_edit.setEchoMode(QLineEdit.EchoMode.Normal)
            self.btn_toggle.setText("HIDE")
        else:
            self.key_edit.setEchoMode(QLineEdit.EchoMode.Password)
            self.btn_toggle.setText("SHOW")

    def get_settings(self) -> dict:
        custom = self.custom_model.text().strip()
        return {
            "provider": "Groq" if self.btn_groq.isChecked() else "OpenRouter",
            "api_key": self.key_edit.text().strip(),
            "model": custom if custom else self.model_combo.currentText(),
        }

    def save(self):
        s = self.get_settings()
        try:
            self.config_path.write_text(json.dumps(s), encoding="utf-8")
            self.lbl_save_status.setText("✓ Saved")
            self.lbl_save_status.setStyleSheet(f"color: {ACCENT};")
        except Exception as e:
            self.lbl_save_status.setText(f"Save failed: {e}")
        self.settings_changed.emit(s)

    def _load_saved(self):
        if self.config_path.exists():
            try:
                s = json.loads(self.config_path.read_text(encoding="utf-8"))
                if s.get("provider") == "OpenRouter":
                    self.btn_openrouter.setChecked(True)
                self.key_edit.setText(s.get("api_key", ""))
                model = s.get("model", "")
                idx = self.model_combo.findText(model)
                if idx >= 0:
                    self.model_combo.setCurrentIndex(idx)
                else:
                    self.custom_model.setText(model)
            except Exception:
                pass


# ── Main Window ────────────────────────────────────────────────────────────────

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Study Buddy")
        self.resize(1100, 720)
        self.setMinimumSize(800, 560)
        self._build_ui()

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # ── App header ──
        header = QWidget()
        header.setFixedHeight(48)
        header.setStyleSheet(f"background: {BG}; border-bottom: 1px solid {BORDER};")
        hl = QHBoxLayout(header)
        hl.setContentsMargins(20, 0, 20, 0)

        logo = QLabel("◆ STUDY BUDDY")
        logo.setStyleSheet(f"color: {ACCENT}; font-size: 14px; letter-spacing: 3px; font-weight: bold;")
        hl.addWidget(logo)
        hl.addStretch()

        version = QLabel("v0.2.0")
        version.setStyleSheet(f"color: {TEXT_DARK}; font-size: 11px;")
        hl.addWidget(version)

        main_layout.addWidget(header)

        # ── Tabs ──
        self.settings_data = {}
        self.settings_tab = SettingsTab()
        self.settings_tab.settings_changed.connect(self._on_settings_changed)
        self.settings_data = self.settings_tab.get_settings()

        self.flashcard_tab = FlashcardTab(self.settings_data)

        tabs = QTabWidget()
        tabs.setDocumentMode(True)
        tabs.addTab(QuizTab(), "Quiz")
        tabs.addTab(self.flashcard_tab, "Flashcards")
        tabs.addTab(self.settings_tab, "Settings")
        tabs.currentChanged.connect(self._on_tab_change)

        main_layout.addWidget(tabs)

        self.tabs = tabs

    def _on_settings_changed(self, s: dict):
        self.settings_data.update(s)
        self.flashcard_tab.settings = self.settings_data
        self.flashcard_tab.update_api_status()

    def _on_tab_change(self, idx: int):
        if idx == 1:
            self.flashcard_tab.update_api_status()


# ── Entry ──────────────────────────────────────────────────────────────────────

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Study Buddy")
    app.setStyleSheet(STYLESHEET)

    # macOS: ensure menu bar works natively
    if sys.platform == "darwin":
        app.setAttribute(Qt.ApplicationAttribute.AA_DontShowIconsInMenus, True)

    win = MainWindow()
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
