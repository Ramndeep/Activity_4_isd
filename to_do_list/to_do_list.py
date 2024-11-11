from PySide6.QtWidgets import QMainWindow, QLineEdit, QPushButton, QTableWidget, QLabel, QMessageBox, QVBoxLayout, QWidget, QTableWidgetItem, QComboBox
from PySide6.QtCore import Slot
from to_do_list.task_editor import TaskEditor
import csv

class ToDoList(QMainWindow):
    def __init__(self):
        super().__init__()
        self.__initialize_widgets()

        # Connect buttons to their respective event handlers
        self.add_button.clicked.connect(self.on_add_task)
        self.task_table.cellClicked.connect(self.on_edit_task)
        self.save_button.clicked.connect(self.__save_to_csv)

    def __initialize_widgets(self):
        """
        Sets up the layout and widgets for the ToDoList window.
        """
        self.setWindowTitle("To-Do List")

        self.task_input = QLineEdit(self)
        self.task_input.setPlaceholderText("New Task")

        self.status_combo = QComboBox(self)
        self.status_combo.addItems(["Backlog", "In Progress", "Done"])

        self.add_button = QPushButton("Add Task", self)
        self.save_button = QPushButton("Save to CSV", self)

        self.task_table = QTableWidget(self)
        self.task_table.setColumnCount(2)
        self.task_table.setHorizontalHeaderLabels(["Task", "Status"])

        self.status_label = QLabel(self)

        layout = QVBoxLayout()
        layout.addWidget(self.task_input)
        layout.addWidget(self.status_combo)
        layout.addWidget(self.add_button)
        layout.addWidget(self.task_table)
        layout.addWidget(self.save_button)
        layout.addWidget(self.status_label)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    @Slot()
    def on_add_task(self):
        """
        Adds a new task to the task table when 'Add Task' button is clicked.
        """
        task = self.task_input.text().strip()
        status = self.status_combo.currentText()

        if task:
            row_position = self.task_table.rowCount()
            self.task_table.insertRow(row_position)
            self.task_table.setItem(row_position, 0, QTableWidgetItem(task))
            self.task_table.setItem(row_position, 1, QTableWidgetItem(status))
            self.status_label.setText(f"Added task: {task}")
            self.task_input.clear()
        else:
            self.status_label.setText("Please enter a task and select its status.")

    @Slot(int, int)
    def on_edit_task(self, row, column):
        """
        Opens the TaskEditor dialog to edit the status of the selected task.
        """
        current_status = self.task_table.item(row, 1).text()
        editor = TaskEditor(row, current_status)
        editor.task_updated.connect(self.update_task_status)
        editor.exec()

    @Slot(int, str)
    def update_task_status(self, row, new_status):
        """
        Updates the status of a task in the task table.
        """
        self.task_table.setItem(row, 1, QTableWidgetItem(new_status))
        self.status_label.setText(f"Task status updated to: {new_status}")

    def __load_data(self, file_path: str):
        """
        Loads data from a CSV file and adds each row to the task table.
        """
        with open(file_path, newline='') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Skip the header
            for row in reader:
                self.__add_table_row(row)

    def __add_table_row(self, row_data):
        """
        Adds a row of data to the task table.
        """
        row_position = self.task_table.rowCount()
        self.task_table.insertRow(row_position)
        self.task_table.setItem(row_position, 0, QTableWidgetItem(row_data[0]))
        self.task_table.setItem(row_position, 1, QTableWidgetItem(row_data[1]))

    def __save_to_csv(self):
        """
        Saves the current task table data to a CSV file.
        """
        file_path = 'output/todos.csv'
        with open(file_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Task", "Status"])  # Header
            for row in range(self.task_table.rowCount()):
                task = self.task_table.item(row, 0).text()
                status = self.task_table.item(row, 1).text()
                writer.writerow([task, status])
        self.status_label.setText("Tasks saved to todos.csv")
