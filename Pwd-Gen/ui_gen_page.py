#Create the generate password page feature
'''
Replace dialog functionality with page widget
'''

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QSlider, QCheckBox
)
from PySide6.QtCore import Qt
import random
import string

class GeneratePasswordPage(QWidget):
    def __init__(self, backend, cipher, settings, parent=None):
        super().__init__(parent)

        self.backend = backend
        self.cipher = cipher
        self.setWindowTitle("Generate Password")
        self.setMinimumWidth(420)

        layout = QVBoxLayout(self)

        # Label input
        layout.addWidget(QLabel("Label:"))
        self.label_input = QLineEdit()
        layout.addWidget(self.label_input)

        # Length slider
        layout.addWidget(QLabel("Length:"))
        self.length_slider = QSlider(Qt.Horizontal)
        self.length_slider.setMinimum(6)
        self.length_slider.setMaximum(32)
        self.length_slider.setValue(12)
        self.length_slider.valueChanged.connect(self.update_strength)
        layout.addWidget(self.length_slider)

        # Character toggles
        self.lower_cb = QCheckBox("Lowercase")
        self.upper_cb = QCheckBox("Uppercase")
        self.number_cb = QCheckBox("Numbers")
        self.symbol_cb = QCheckBox("Symbols")

        for cb in (self.lower_cb, self.upper_cb, self.number_cb, self.symbol_cb):
            cb.setChecked(True)
            cb.stateChanged.connect(self.update_strength)
            layout.addWidget(cb)

        # Generate password display
        layout.addWidget(QLabel("Generated Password:"))
        self.password_display = QLineEdit()
        self.password_display.setReadOnly(True)
        layout.addWidget(self.password_display)

        # Strength meter
        self.strength_label = QLabel("Strength: [----------] 0/10")
        layout.addWidget(self.strength_label)

        # Buttons
        btn_layout = QHBoxLayout()
        self.generate_btn = QPushButton("Generate")
        self.save_btn = QPushButton("Save")
        self.save_btn.setEnabled(False)

        self.generate_btn.clicked.connect(self.generate_password)
        self.save_btn.clicked.connect(self.save_password)

        btn_layout.addWidget(self.generate_btn)
        btn_layout.addWidget(self.save_btn)
        layout.addLayout(btn_layout)

        # Initial strength update
        self.update_strength()

        # Default settings
        self.length_slider.setValue(settings["default_length"])
        self.lower_cb.setChecked(settings["lowercase"])
        self.upper_cb.setChecked(settings["uppercase"])
        self.number_cb.setChecked(settings["numbers"])
        self.symbol_cb.setChecked(settings["symbols"])

    # Build character set
    def build_character(self):
        chars = ""
        if self.lower_cb.isChecked():
            chars += string.ascii_lowercase
        if self.upper_cb.isChecked():
            chars += string.ascii_uppercase
        if self.number_cb.isChecked():
            chars += string.digits
        if self.symbol_cb.isChecked():
            chars += string.punctuation
        return chars
    
    # Generate password
    def generate_password(self):
        chars = self.build_character()
        length = self.length_slider.value()

        if not chars:
            self.password_display.setText("No character types selected")
            self.save_btn.setEnabled(False)
            return
        pwd = ''.join(random.choice(chars) for _ in range(length))
        self.password_display.setText(pwd)
        self.update_strength()
        self.save_btn.setEnabled(True)

    # Strength meter
    def update_strength(self):
        pwd = self.password_display.text()
        score = self.calculate_strength(pwd)

        meter = "#" * score + "_" * (10 - score)

        if score <= 3:
            color = "red"
            label = "Weak"
        elif score <= 6:
            color = "orange"
            label = "Medium"
        else:
            color = "green"
            label = "Strong"
        
        self.strength_label.setText(
            f"<span style='color:{color}'>Strength: [{meter}] {score}/10 ({label})</span>"
        )

    def calculate_strength(self, pwd):
        if not pwd:
            return 0
        score = 0

        if len(pwd) >= 8: score += 2
        if len(pwd) >= 12: score += 2
        if len(pwd) >= 16: score += 2
        if any(c.islower() for c in pwd): score += 1
        if any(c.isupper() for c in pwd): score += 1
        if any(c.isdigit() for c in pwd): score += 1
        if any(c in string.punctuation for c in pwd): score += 1

        # Repetition penalty
        if len(set(pwd)) < len(pwd) * 0.6: score -= 1
        
        return max(0, min(score, 10))
    
    # Save password
    def save_password(self):
        label = self.label_input.text().strip()
        pwd = self.password_display.text().strip()

        if not label or not pwd:
            return
        
        self.backend.save_password(label, pwd, self.cipher)
        self.accept()