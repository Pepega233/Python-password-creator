import sys,os
import string
import secrets
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QPushButton, QLineEdit,
    QCheckBox, QVBoxLayout, QHBoxLayout, QWidget
)
from PySide6.QtGui import QGuiApplication, QIcon  # potrebné na clipboard

# ============================
#   LOGIKA GENEROVANIA HESLA
# ============================
def password_generator(length, lowercase, uppercase, digits, symbols):
    allowed = ""

    if lowercase:
        allowed += string.ascii_lowercase
    if uppercase:
        allowed += string.ascii_uppercase
    if digits:
        allowed += string.digits
    if symbols:
        allowed += string.punctuation

    if not allowed:
        return "Select at least one character type!"

    password = "".join(secrets.choice(allowed) for _ in range(length))
    return password


class DemoWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Password Generator")
        self.setGeometry(300, 300, 300, 200)
        self.setWindowIcon(QIcon("logo.png"))
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)


        def add_widget_with_label(layout, widget, label_text):
            hbox = QHBoxLayout()
            label = QLabel(label_text)
            hbox.addWidget(label)
            hbox.addWidget(widget)
            layout.addLayout(hbox)


        self.length_input = QLineEdit()
        self.length_input.setPlaceholderText("Enter length (e.g. 20)")
        add_widget_with_label(main_layout, self.length_input, "Length:")


        self.lowercase_box = QCheckBox("Lowercase")
        add_widget_with_label(main_layout, self.lowercase_box, "Option:")

        self.uppercase_box = QCheckBox("Uppercase")
        add_widget_with_label(main_layout, self.uppercase_box, "Option:")

        self.digits_box = QCheckBox("Digits")
        add_widget_with_label(main_layout, self.digits_box, "Option:")

        self.symbols_box = QCheckBox("Symbols")
        add_widget_with_label(main_layout, self.symbols_box, "Option:")


        self.output_label = QLabel("Your password will appear here")
        main_layout.addWidget(self.output_label)


        self.button = QPushButton("Generate Password")
        self.button.clicked.connect(self.on_generate_clicked)
        main_layout.addWidget(self.button)


        self.copy_button = QPushButton("Copy")
        self.copy_button.clicked.connect(self.copy_to_clipboard)
        main_layout.addWidget(self.copy_button)

    def on_generate_clicked(self):
        try:
            length = int(self.length_input.text())
        except ValueError:
            self.output_label.setText("Length must be a number!")
            return

        password = password_generator(
            length,
            self.lowercase_box.isChecked(),
            self.uppercase_box.isChecked(),
            self.digits_box.isChecked(),
            self.symbols_box.isChecked()
        )

        self.output_label.setText(password)

    def copy_to_clipboard(self):
        text = self.output_label.text()
        QGuiApplication.clipboard().setText(text)
        self.output_label.setText(f"{text}  (copied ✔)")


def resource_path(relative):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative)
    return os.path.join(os.path.abspath("."), relative)

app = QApplication(sys.argv)
style_file = resource_path("style.qss")
with open(style_file, "r") as f:
    app.setStyleSheet(f.read())
window = DemoWindow()
window.show()
sys.exit(app.exec())
