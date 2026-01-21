#Create GUI for random password generator.
#Use .
'''
Create basic layout with sidebar and main content area.
'''
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, 
    QHBoxLayout, QListWidget, 
    QStackedWidget, QLabel
)

import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Password Manager")
        self.setMinimumSize(900, 600)

        # Main Container
        main_widget = QWidget()
        main_layout = QHBoxLayout(main_widget)

        # Sidebar
        self.sidebar = QListWidget()
        self.sidebar.setFixedWidth(200)
        self.sidebar.addItem("Generate Password")
        self.sidebar.addItem("Saved Passwords")
        self.sidebar.addItem("Search")
        self.sidebar.addItem("Settings")
        self.sidebar.addItem("Import")
        self.sidebar.addItem("Export")
        self.sidebar.addItem("Exit")
        self.sidebar.currentRowChanged.connect(self.switch_page)

        # Stacked pages
        self.pages = QStackedWidget()

        # Placeholder pages to be replaced
        self.page_generate = QLabel("Generate Password Page")
        self.page_saved = QLabel("Saved Passwords Page")
        self.page_search = QLabel("Search Page")
        self.page_settings = QLabel("Settings Page")
        self.page_import = QLabel("Import Page")
        self.page_export = QLabel("Export Page")

        self.pages.addWidget(self.page_generate)
        self.pages.addWidget(self.page_saved)
        self.pages.addWidget(self.page_search)
        self.pages.addWidget(self.page_settings)
        self.pages.addWidget(self.page_import)
        self.pages.addWidget(self.page_export)

        # Add sidebar + pages to layout
        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(self.pages)

        self.setCentralWidget(main_widget)
    
    def switch_page(self, index):
        if index == 6: # Exit
            self.close()
        else:
            self.pages.setCurrentIndex(index)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())