import sys
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QLabel,
    QMenuBar,
    QWidget,
    QVBoxLayout,
)


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

        file_menu = menu_bar.addMenu("File")
        help_menu = menu_bar.addMenu("Help")

    def _setup_ui(self):
        central_widget = QWidget()
        layout = QVBoxLayout()

        placeholder_label = QLabel("Application skeleton initialized.")
        placeholder_label.setAlignment(Qt.AlignCenter)

        layout.addWidget(placeholder_label)
        central_widget.setLayout(layout)

        self.setCentralWidget(central_widget)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
