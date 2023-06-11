from PyQt6.QtWidgets import QApplication, QLabel, QWidget, \
    QGridLayout, QLineEdit, QPushButton, QMainWindow, \
    QTableWidget, QTableWidgetItem, QDialog, QVBoxLayout
from PyQt6.QtGui import QAction
import sys
import sqlite3

# Constants
DB = db = "G:\\Users\\valen\\Documents\\Valen\\python\\python-mega-course\\student-management-system\\db\\database.db"


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management System")

        # Add menus
        file_menu_item = self.menuBar().addMenu("&File")
        help_menu_item = self.menuBar().addMenu("&Help")

        # Add actions to the menu (these are submenu items).
        add_student_action = QAction("Add Student", self)
        add_student_action.triggered.connect(self.insert)
        file_menu_item.addAction(add_student_action)
        about_action = QAction("About", self)
        help_menu_item.addAction(about_action)

        # Add the main table to the GUI.
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("ID", "Name", "Course", "Mobile"))
        self.table.verticalHeader().setVisible(False)
        self.setCentralWidget(self.table)

    def load_data(self):
        """Populates the central widget with data."""
        connection = sqlite3.connect(DB)
        result = connection.execute("SELECT * FROM students")
        # The line below ensures that the load_data method does not
        # duplicate information in the central widget.
        self.table.setRowCount(0)
        for row_no, row_data in enumerate(result):
            self.table.insertRow(row_no)
            for col_no, col_data in enumerate(row_data):
                self.table.setItem(row_no, col_no, QTableWidgetItem(str(col_data)))
        connection.close()

    def insert(self):
        print(f"Add student clicked")
        dialog = InsertDialog()
        dialog.exec()


class InsertDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Insert Student Data")
        self.setFixedWidth(300)
        self.setFixedHeight(300)
        # This is a purely vertical widget layout.
        layout = QVBoxLayout()

        # Add widgets to the layout since this is a dialog window.
        student_name = QLineEdit()
        student_name.setPlaceholderText("Name")
        layout.addWidget(student_name)

        self.setLayout(layout)


app = QApplication(sys.argv)
management_system = MainWindow()
management_system.show()
management_system.load_data()
sys.exit(app.exec())
