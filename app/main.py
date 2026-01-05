import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QMenuBar
from PySide6.QtCore import Qt

from ui.chat_widget import ChatWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Offline Security Report Generator")
        self.resize(900, 600)

        self._setup_menu()
        self._setup_ui()

    def _setup_menu(self):
        menu_bar = QMenuBar(self)
        self.setMenuBar(menu_bar)

        menu_bar.addMenu("File")
        menu_bar.addMenu("Help")

    def _setup_ui(self):
        # Phase 6: temporary direct wiring to chat widget
        self.setCentralWidget(ChatWidget(model_id="mistral:7b"))


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
