from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QLabel, QWidget, \
    QGridLayout, QLineEdit, QPushButton, QMainWindow, \
    QTableWidget, QTableWidgetItem, QDialog, QVBoxLayout, \
    QComboBox, QToolBar, QStatusBar, QMessageBox
from PyQt6.QtGui import QAction, QIcon
import sys
import sqlite3

# Constants
DB = db = "G:\\Users\\valen\\Documents\\Valen\\python\\python-mega-course\\student-management-system\\db\\database.db"


class DatabaseConnection:
    def __init__(self, database_file=DB):
        self.database_file = database_file

    def connect(self):
        connection = sqlite3.connect(self.database_file)
        return connection


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management System")
        self.setMinimumSize(800, 600)

        # Add menus
        file_menu_item = self.menuBar().addMenu("&File")
        help_menu_item = self.menuBar().addMenu("&Help")
        edit_menu_item = self.menuBar().addMenu("&Edit")

        # Add actions to the menu (these are submenu items).
        add_student_action = QAction(QIcon("icons/add.png"), "Add Student", self)
        add_student_action.triggered.connect(self.insert)
        file_menu_item.addAction(add_student_action)
        about_action = QAction("About", self)
        about_action.triggered.connect(self.about)
        help_menu_item.addAction(about_action)
        search_action = QAction(QIcon("icons/search.png"), "Search", self)
        search_action.triggered.connect(self.search)
        edit_menu_item.addAction(search_action)

        # Add the main table to the GUI.
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("ID", "Name", "Course", "Mobile"))
        self.table.verticalHeader().setVisible(False)
        self.setCentralWidget(self.table)

        # Create toolbar and add toolbar elements to toolbar.
        toolbar = QToolBar()
        toolbar.setMovable(True)
        self.addToolBar(toolbar)
        toolbar.addAction(add_student_action)
        toolbar.addAction(search_action)

        # Create status bar.
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)

        # Detect a cell click.
        self.table.cellClicked.connect(self.cell_clicked)

    def load_data(self):
        """Populates the central widget with data."""
        connection = DatabaseConnection().connect()
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

    def cell_clicked(self):
        edit_button = QPushButton("Edit Record")
        edit_button.clicked.connect(self.edit)
        delete_button = QPushButton("Delete Record")
        delete_button.clicked.connect(self.delete)

        # buttons is used instead of children in case we
        # need to add a similar stanza to eliminate QLabel
        # widgets later on.
        buttons = self.findChildren(QPushButton)
        if buttons:
            for child in buttons:
                self.statusbar.removeWidget(child)

        self.statusbar.addWidget(edit_button)
        self.statusbar.addWidget(delete_button)

    def edit(self):
        dialog = EditDialog()
        dialog.exec()

    def delete(self):
        dialog = DeleteDialog()
        dialog.exec()

    def about(self):
        dialog = AboutDialog()
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
        connection = DatabaseConnection().connect()
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
        name = self.student_name.text()
        connection = DatabaseConnection().connect()
        cursor = connection.cursor()
        result = cursor.execute("SELECT * FROM students WHERE name = ?", (name,))
        rows = list(result)
        print(f"rows: {rows}")
        items = main_window.table.findItems(name, Qt.MatchFlag.MatchFixedString)
        for item in items:
            print(f"item: {item}")
            main_window.table.item(item.row(), 1).setSelected(True)

        cursor.close()
        connection.close()


class EditDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Update Student Data")
        self.setFixedWidth(300)
        self.setFixedHeight(300)
        # This is a purely vertical widget layout.
        layout = QVBoxLayout()

        # Get student name from selected row.
        index = main_window.table.currentRow()
        student_name = main_window.table.item(index, 1).text()

        # Add student name widget to layout with student's original data in place.
        self.student_name = QLineEdit(student_name)
        layout.addWidget(self.student_name)

        # Get course data from selected row.
        course_name = main_window.table.item(index, 2).text()

        # Add combo box of courses to layout with student's original data in place.
        self.course_name = QComboBox()
        courses = ["Biology", "Math", "Astronomy", "Physics"]
        self.course_name.addItems(courses)
        self.course_name.setCurrentText(course_name)
        layout.addWidget(self.course_name)

        # Get cell phone data from selected row.
        cell_phone_no = main_window.table.item(index, 3).text()

        # Add mobile widget to layout with student's original data in place.
        self.mobile = QLineEdit(cell_phone_no)
        self.mobile.setPlaceholderText("Cell Phone Number")
        layout.addWidget(self.mobile)

        # Get ID from selected row.
        self.student_id = main_window.table.item(index, 0).text()

        # Add submit button to layout.
        button = QPushButton("Update Record")
        button.clicked.connect(self.update_student)
        layout.addWidget(button)

        self.setLayout(layout)

    def update_student(self):
        connection = DatabaseConnection().connect()
        cursor = connection.cursor()
        cursor.execute("UPDATE students SET name = ?, course = ?, mobile = ? WHERE id =?",
                       (self.student_name.text(),
                        self.course_name.itemText(self.course_name.currentIndex()),
                        self.mobile.text(),
                        self.student_id))
        connection.commit()
        cursor.close()
        connection.close()
        # Refresh table.
        main_window.load_data()


class DeleteDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Delete Student Data")

        layout = QGridLayout()
        confirmation = QLabel("Are you sure you want to delete this record?")
        yes = QPushButton("Yes")
        no = QPushButton("No")

        layout.addWidget(confirmation, 0, 0, 1, 2)
        layout.addWidget(yes, 1, 0)
        layout.addWidget(no, 1, 1)
        self.setLayout(layout)

        yes.clicked.connect(self.delete_student)
        no.clicked.connect(self.close)

    def delete_student(self):
        # Get selected row index and student ID.
        index = main_window.table.currentRow()
        student_id = main_window.table.item(index, 0).text()

        connection = DatabaseConnection().connect()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM students WHERE id = ?", (student_id,))
        connection.commit()
        cursor.close()
        connection.close()
        main_window.load_data()
        self.close()

        confirmation_widget = QMessageBox()
        confirmation_widget.setWindowTitle("Success")
        confirmation_widget.setText("The record was deleted successfully.")
        confirmation_widget.exec()


class AboutDialog(QMessageBox):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("About")
        content = """
        This app was created during the course "Python Mega Course".
        Feel free to modify and reuse this app.
        """
        self.setText(content)


app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
main_window.load_data()
sys.exit(app.exec())
