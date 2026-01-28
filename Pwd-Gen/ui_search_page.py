# Create a search page that allows the user to query and filter their results
'''
Add features:
Search bar, Result filter, Display results in table,
Pull data from encrypted backend,
Reuse strength-meter logic
'''

from PySide6.QtWidgets import(
    QWidget, QVBoxLayout, QHBoxLayout, QLineEdit,
    QPushButton, QTableWidget, QTableWidgetItem,
    QHeaderView
)
from PySide6.QtCore import Qt
import string

class SearchPage(QWidget):
    def __init__(self, backend, cipher):
        super().__init__()

        self.backend = backend
        self.cipher = cipher

        layout = QVBoxLayout(self)

        # Search bar
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by label...")
        self.search_btn = QPushButton("Search")

        self.search_btn.clicked.connect(self.perform_search)
        self.search_input.returnPressed.connect(self.perform_search)

        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.search_btn)
        layout.addLayout(search_layout)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Label", "Password", "Strength", "Reveal"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setAlternatingRowColors(True)

        layout.addWidget(self.table)

    # Perform search
    def perform_search(self):
        term = self.search_input.text().strip().lower()
        self.table.setRowCount(0)

        entries = self.backend.load_all_passwords(self.cipher)

        for label, password in entries:
            if term in label.lower():
                self.add_row(label, password)

    # Add a row to the table
    def add_row(self, label, password):
        row = self.table.rowCount()
        self.table.insertRow(row)

        # Label
        self.table.setItem(row, 0, QTableWidgetItem(label))

        # Masked password
        masked = "•" *len(password)
        pwd_item = QTableWidgetItem(masked)
        pwd_item.setData(Qt.UserRole, password)
        self.table.setItem(row, 1, pwd_item)

        # Strength
        strength = self.calculate_strength(password)
        self.table.setItem(row, 2, QTableWidgetItem(strength))

        # Reveal
        reveal_btn = QPushButton("Show")
        reveal_btn.clicked.connect(lambda _, r=row: self.toggle_reveal(r))
        self.table.setCellWidget(row, 3, reveal_btn)

    # Reveal and hide password
    def toggle_reveal(self, row):
        item = self.table.item(row, 1)
        real_pwd = item.data(Qt.UserRole)

        if item.text().startswith("•"):
            item.setText(real_pwd)
        else:
            item.setText("•" * len(real_pwd))

    # Strength meter (basic from SavedPasswordsPage)
    def calculate_strength(self, pwd):
                score = 0

                if len(pwd) >= 8: score += 2
                if len(pwd) >= 12: score += 2
                if len(pwd) >= 16: score += 2
                if any(c.islower() for c in pwd): score += 1
                if any(c.isupper() for c in pwd): score += 1
                if any(c.isdigit() for c in pwd): score += 1
                if any(c in string.punctuation for c in pwd): score += 1

                if len(set(pwd)) < len(pwd) * 0.6: score -= 1
                score = max(0, min(score, 10))

                if score <= 3:
                    return "Weak"
                elif score <= 6:
                    return "Medium"
                else:
                    return "Strong"