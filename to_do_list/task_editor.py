from PySide6.QtWidgets import QPushButton, QVBoxLayout, QComboBox, QDialog
from PySide6.QtCore import Signal, Slot

class TaskEditor(QDialog):
    # Signal to emit when the task's status is updated
    task_updated = Signal(int, str)

    def __init__(self, row: int, status: str):
        """
        Initializes the TaskEditor dialog for editing a task's status.

        Args:
            row (int): The row of the task in the main task table.
            status (str): The current status of the task.
        """
        super().__init__()
        self.row = row  # Store the row number
        self.initialize_widgets(status)

    def initialize_widgets(self, status: str):
        """
        Sets up the layout and widgets for the TaskEditor dialog.
        """
        self.setWindowTitle("Edit Task Status")

        # Status dropdown (status_combo)
        self.status_combo = QComboBox(self)
        self.status_combo.addItems(["Backlog", "In Progress", "Done"])
        self.status_combo.setCurrentText(status)  # Set to current status

        # Save button (save_button)
        self.save_button = QPushButton("Save", self)
        self.save_button.clicked.connect(self.save_status)  # Connect to slot

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.status_combo)
        layout.addWidget(self.save_button)
        self.setLayout(layout)
        self.setFixedWidth(150)

    @Slot()
    def save_status(self):
        """
        Emits the task_updated signal with the updated status and closes the dialog.
        """
        new_status = self.status_combo.currentText()  # Get new status
        self.task_updated.emit(self.row, new_status)  # Emit the signal with row and status
        self.accept()  # Close the dialog
