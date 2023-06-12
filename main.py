from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QLabel, QWidget, \
    QGridLayout, QLineEdit, QPushButton, QMainWindow, \
    QTableWidget, QTableWidgetItem, QDialog, QVBoxLayout, \
    QComboBox
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
        edit_menu_item = self.menuBar().addMenu("&Edit")

        # Add actions to the menu (these are submenu items).
        add_student_action = QAction("Add Student", self)
        add_student_action.triggered.connect(self.insert)
        file_menu_item.addAction(add_student_action)
        about_action = QAction("About", self)
        help_menu_item.addAction(about_action)
        search_action = QAction("Search", self)
        search_action.triggered.connect(self.search)
        edit_menu_item.addAction(search_action)

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

    def search(self):
        print(f"Search clicked")
        dialog = SearchDialog()
        dialog.exec()


class InsertDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Insert Student Data")
        self.setFixedWidth(300)
        self.setFixedHeight(300)
        # This is a purely vertical widget layout.
        layout = QVBoxLayout()

        # Add student name widget to layout.
        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)

        # Add combo box of courses to layout.
        self.course_name = QComboBox()
        courses = ["Biology", "Math", "Astronomy", "Physics"]
        self.course_name.addItems(courses)
        layout.addWidget(self.course_name)

        # Add mobile widget to layout.
        self.mobile = QLineEdit()
        self.mobile.setPlaceholderText("Cell Phone Number")
        layout.addWidget(self.mobile)

        # Add submit button to layout.
        button = QPushButton("Submit")
        button.clicked.connect(self.add_student)
        layout.addWidget(button)

        self.setLayout(layout)

    def add_student(self):
        name = self.student_name.text()
        course = self.course_name.itemText(self.course_name.currentIndex())
        mobile = self.mobile.text()
        connection = sqlite3.connect(DB)
        cursor = connection.cursor()
        cursor.execute("INSERT INTO students (name, course, mobile) VALUES (?, ?, ?)",
                       (name, course, mobile))
        connection.commit()
        cursor.close()
        connection.close()
        main_window.load_data()


class SearchDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Search by Student Name")
        self.setFixedWidth(300)
        self.setFixedHeight(300)
        # This is a purely vertical widget layout.
        layout = QVBoxLayout()

        # Add student name widget to layout.
        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)

        button = QPushButton("Search")
        button.clicked.connect(self.search)
        layout.addWidget(button)

        self.setLayout(layout)

    def search(self):
        pass


app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
main_window.load_data()
sys.exit(app.exec())
