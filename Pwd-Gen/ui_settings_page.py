# Create a settings page tha allows user to default settings and save settings
'''
Add features:
Default password length, Toggles for character sets,
"Save Settings" button, Auto-integration with generator
dialog
'''

from PySide6.QtWidgets import(
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QSlider, QCheckBox, QPushButton
)
from PySide6.QtCore import Qt
import json
import os

SETTINGS_FILE = "settings.json"

class SettingsPage(QWidget):
    def __init__(self):
        super().__init__()
        
        layout = QVBoxLayout(self)

        # Title
        layout.addWidget(QLabel("<b>Password Generator Settings</b>"))

        # Default length
        layout.addWidget(QLabel("Default Password Length:"))
        self.length_slider = QSlider(Qt.Horizontal)
        self.length_slider.setMinimum(6)
        self.length_slider.setMaximum(32)
        self.length_slider.setValue(12)
        layout.addWidget(self.length_slider)

        # Character set toggles
        self.lower_cb = QCheckBox("Include lowercase")
        self.upper_cb = QCheckBox("Include uppercase")
        self.number_cb = QCheckBox("Include numbers")
        self.symbol_cb = QCheckBox("Include symbols")

        for cb in (self.lower_cb, self.upper_cb, self.number_cb, self. symbol_cb):
            cb.setChecked(True)
            layout.addWidget(cb)
        
        # Save button
        self.save_btn = QPushButton("Save Settings")
        self.save_btn.clicked.connect(self.save_settings)
        layout.addWidget(self.save_btn)

        layout.addStretch()

        # Load existing settings
        self.load_setting()

    # Save settings to JSON file
    def save_settings(self):
        settings = {
            "default_length": self.length_slider.value(),
            "lowercase": self.lower_cb.isChecked(),
            "uppercase": self.upper_cb.isChecked(),
            "numbers": self.number_cb.isChecked(),
            "symbols": self.symbol_cb.isChecked()
        }

        with open(SETTINGS_FILE, "w") as f:
            json.dump(settings, f, indent=4)
    
    # Load settings from JSON file
    def load_setting(self):
        if not os.path.exists(SETTINGS_FILE):
            return
        
        with open(SETTINGS_FILE, "r") as f:
            settings = json.load(f)
        
        self.length_slider.setValue(settings.get("default_length", 12))
        self.lower_cb.setChecked(settings.get("lowercase", True))
        self.upper_cb.setChecked(settings.get("uppercase", True))
        self.number_cb.setChecked(settings.get("numbers", True))
        self.symbol_cb.setChecked(settings.get("symbols", True))