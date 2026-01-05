import json
import requests
from PySide6.QtGui import QTextCursor
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QTextEdit,
    QLineEdit,
    QPushButton,
    QHBoxLayout,
)
from PySide6.QtCore import QThread, Signal


class InferenceThread(QThread):
    token_received = Signal(str)
    finished_cleanly = Signal()
    error_occurred = Signal(str)

    def __init__(self, model_id: str, prompt: str):
        super().__init__()
        self.model_id = model_id
        self.prompt = prompt
        self._stop_requested = False

    def stop(self):
        self._stop_requested = True

    def run(self):
        try:
            response = requests.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": self.model_id,
                    "prompt": self.prompt,
                    "stream": True,
                },
                stream=True,
                timeout=60,
            )

            for line in response.iter_lines():
                if self._stop_requested:
                    break

                if not line:
                    continue

                data = json.loads(line.decode("utf-8"))

                token = data.get("response")
                if token:
                    self.token_received.emit(token)

                if data.get("done"):
                    break

            self.finished_cleanly.emit()

        except Exception as exc:
            self.error_occurred.emit(str(exc))


class ChatWidget(QWidget):
    def __init__(self, model_id: str):
        super().__init__()
        self.model_id = model_id
        self._thread: InferenceThread | None = None

        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout()

        self.chat_area = QTextEdit()
        self.chat_area.setReadOnly(True)

        self.input_line = QLineEdit()
        self.input_line.setPlaceholderText("Enter your prompt…")

        self.send_button = QPushButton("Send")
        self.stop_button = QPushButton("Stop")
        self.reset_button = QPushButton("Reset Session")

        button_row = QHBoxLayout()
        button_row.addWidget(self.send_button)
        button_row.addWidget(self.stop_button)
        button_row.addWidget(self.reset_button)

        layout.addWidget(self.chat_area)
        layout.addWidget(self.input_line)
        layout.addLayout(button_row)

        self.setLayout(layout)

        self.send_button.clicked.connect(self._send_prompt)
        self.stop_button.clicked.connect(self._stop_generation)
        self.reset_button.clicked.connect(self._reset_session)

    def _send_prompt(self):
        prompt = self.input_line.text().strip()
        if not prompt:
            return

        self.chat_area.append(f"> {prompt}")
        self.input_line.clear()

        self._thread = InferenceThread(self.model_id, prompt)
        self._thread.token_received.connect(self._append_token)
        self._thread.error_occurred.connect(self._show_error)
        self._thread.start()

    def _append_token(self, token: str):
        self.chat_area.moveCursor(QTextCursor.End)
        self.chat_area.insertPlainText(token)

    def _show_error(self, message: str):
        self.chat_area.append(f"\n[ERROR] {message}\n")

    def _stop_generation(self):
        if self._thread:
            self._thread.stop()

    def _reset_session(self):
        if self._thread:
            self._thread.stop()
            self._thread = None
        self.chat_area.clear()
