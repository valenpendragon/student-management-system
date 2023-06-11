from PyQt6.QtWidgets import QApplication, QLabel, QWidget, \
    QGridLayout, QLineEdit, QPushButton, QMainWindow, \
    QTableWidget
from PyQt6.QtGui import QAction
import sys
import sqlite3


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management System")

        # Add menus
        file_menu_item = self.menuBar().addMenu("&File")
        help_menu_item = self.menuBar().addMenu("&Help")

        # Add actions to the menu (these are submenu items).
        add_student_action = QAction("Add Student", self)
        file_menu_item.addAction(add_student_action)
        about_action = QAction("About", self)
        help_menu_item.addAction(about_action)

        # Add the main table to the GUI.
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("ID", "Name", "Course", "Mobile"))
        self.setCentralWidget(self.table)

        # Populate the table.

    def load_data(self):
        pass


app = QApplication(sys.argv)
management_system = MainWindow()
management_system.show()
sys.exit(app.exec())
