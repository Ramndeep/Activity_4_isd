from PySide6.QtWidgets import QMainWindow, QLineEdit, QPushButton, QTableWidget, QLabel, QVBoxLayout, QWidget, QTableWidgetItem, QComboBox
from PySide6.QtCore import Slot
from to_do_list.task_editor import TaskEditor
import csv
import os

class ToDoList(QMainWindow):
    """
    ToDoList application window allowing users to manage and update tasks.
    Users can add tasks with statuses, edit them, and save/load tasks from a CSV file.
    """
    
    def __init__(self):
        """
        Initializes the ToDoList window, setting up the user interface and connecting 
        buttons to their event handlers. Attempts to load task data from 'data/todo.csv'.
        """
        super().__init__()
        self.__initialize_widgets()

        # Connect buttons to their respective event handlers
        self.add_button.clicked.connect(self.on_add_task)
        self.task_table.cellClicked.connect(self.on_edit_task)
        self.save_button.clicked.connect(self.__save_to_csv)  # Connects save_button to __save_to_csv method

        # Load data from 'data/todo.csv' on initialization if file exists
        file_path = 'data/todo.csv'
        if os.path.exists(file_path):
            self.__load_data(file_path)

    def __initialize_widgets(self):
        """
        Sets up the layout and widgets for the main ToDoList window.
        Initializes the task input field, status dropdown, add/save buttons, 
        and the main task table.
        """
        self.setWindowTitle("To-Do List")

        # Task input field
        self.task_input = QLineEdit(self)
        self.task_input.setPlaceholderText("New Task")

        # Status combo box with predefined statuses
        self.status_combo = QComboBox(self)
        self.status_combo.addItems(["Backlog", "In Progress", "Done"])

        # Buttons
        self.add_button = QPushButton("Add Task", self)
        self.save_button = QPushButton("Save to CSV", self)

        # Task table
        self.task_table = QTableWidget(self)
        self.task_table.setColumnCount(2)
        self.task_table.setHorizontalHeaderLabels(["Task", "Status"])

        # Status label for messages
        self.status_label = QLabel(self)

        # Layout setup
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
        Retrieves the task description and status, and adds them to the task table.
        Provides feedback to the user in the status label.
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
        
        Args:
            row (int): The row index of the selected task in the table.
            column (int): The column index of the selected task in the table.
        """
        current_status = self.task_table.item(row, 1).text()
        editor = TaskEditor(row, current_status)
        editor.task_updated.connect(self.update_task_status)
        editor.exec()

    @Slot(int, str)
    def update_task_status(self, row, new_status):
        """
        Updates the status of a task in the task table when edited in TaskEditor.
        
        Args:
            row (int): The row index of the task to update.
            new_status (str): The new status to apply to the task.
        """
        self.task_table.setItem(row, 1, QTableWidgetItem(new_status))
        self.status_label.setText(f"Task status updated to: {new_status}")

    def __load_data(self, file_path: str):
        """
        Loads tasks from a CSV file into the task table.
        
        Args:
            file_path (str): Path to the CSV file containing task data.
        """
        with open(file_path, newline='') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Skip the header row
            for row in reader:
                self.__add_table_row(row)

    def __add_table_row(self, row_data):
        """
        Adds a single row of task data to the task table from a CSV file.
        
        Args:
            row_data (list): List containing the task description and status.
        """
        row_position = self.task_table.rowCount()
        self.task_table.insertRow(row_position)
        self.task_table.setItem(row_position, 0, QTableWidgetItem(row_data[0]))
        self.task_table.setItem(row_position, 1, QTableWidgetItem(row_data[1]))

    def __save_to_csv(self):
        """
        Saves the tasks from the task table to a CSV file in the 'output' directory.
        Iterates through each row in the task table, extracting task and status data, 
        and writes each row to the CSV file.
        """
        # Ensure the output directory exists
        os.makedirs('output', exist_ok=True)
        file_path = 'output/todo.csv'
        
        with open(file_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Task", "Status"])  # Header row
            
            # Iterate through each row in the task table
            for row in range(self.task_table.rowCount()):
                # Extract the task and status text from each cell
                task = self.task_table.item(row, 0).text() if self.task_table.item(row, 0) else ""
                status = self.task_table.item(row, 1).text() if self.task_table.item(row, 1) else ""
                # Write the task and status to the CSV file
                writer.writerow([task, status])
                
        self.status_label.setText("Tasks saved to todo.csv")
