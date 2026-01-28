# Create import-export feature
'''
Export feature:
Copy password vault to a defined location without any encryption
Import feature:
Let user define file and replace password vault with imported file
Automatically refresh Saved Passwords page
'''  
from PySide6.QtWidgets import(
    QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel
)
import shutil
import os

class ImportExportPage(QWidget):
    def __init__(self, refresh_callback=None):
        super().__init__()

        self.refresh_callback = refresh_callback
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("<b>Import / Export Vault </b>"))

        # Export button
        self.export_btn = QPushButton("Export Vault")
        self.export_btn.clicked.connect(self.export_vault)
        layout.addWidget(self.export_btn)

        #Import button
        self.import_btn = QPushButton("Import Vault")
        self.import_btn.clicked.connect(self.import_vault)
        layout.addWidget(self.import_btn)

        layout.addStretch()

    # Export vault
    def export_vault(self):
        if not os.path.exists("passwords.txt"):
            return
        
        path, _ = QFileDialog.getSaveFileName(
            self,
            "Export Vault",
            "vault_backup.txt",
            "Text Files (*.txt)"
        )

        if path:
            shutil.copy("passwords.txt", path)

    # Import Vault
    def import_vault(self):
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Import Vault",
            "",
            "Text Files (*.txt)"
        )

        if path:
            shutil.copy(path, "passwords.txt")

            # Refresh Saved Passwords page
            if self.refresh_callback:
                self.refresh_callback()