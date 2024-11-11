"""
Description: This file defines the ContactList application, allowing users to add, view, and remove contacts. 
The application features a simple UI for managing contacts, displaying each contact's name and phone number in a table.
Author: Ramandeep Kaur
"""

from PySide6.QtCore import Slot
from PySide6.QtWidgets import QMainWindow, QLineEdit, QPushButton, QTableWidget, QLabel, QVBoxLayout, QWidget, QTableWidgetItem, QMessageBox

class ContactList(QMainWindow):
    """
    Contact List Class (QMainWindow). Provides users a 
    way to manage their contacts.
    """
    def __init__(self):
        """
        Initializes a Contact List window in which 
        users can add and remove contact data.
        """
        super().__init__()
        self.__initialize_widgets()      

        # Connect buttons to their respective event handlers
        self.add_button.clicked.connect(self.__on_add_contact)
        self.remove_button.clicked.connect(self.__on_remove_contact)

    def __initialize_widgets(self):
        """
        Given:  Code to create and initialize the QWindow
        and all of the widgets on the window.
        DO NOT EDIT.
        """
        self.setWindowTitle("Contact List")

        self.contact_name_input = QLineEdit(self)
        self.contact_name_input.setPlaceholderText("Contact Name")

        self.phone_input = QLineEdit(self)
        self.phone_input.setPlaceholderText("Phone Number")

        self.add_button = QPushButton("Add Contact", self)
        self.remove_button = QPushButton("Remove Contact", self)
        
        self.contact_table = QTableWidget(self)
        self.contact_table.setColumnCount(2)
        self.contact_table.setHorizontalHeaderLabels(["Name", "Phone"])

        self.status_label = QLabel(self)

        layout = QVBoxLayout()
        layout.addWidget(self.contact_name_input)
        layout.addWidget(self.phone_input)
        layout.addWidget(self.add_button)
        layout.addWidget(self.remove_button)
        layout.addWidget(self.contact_table)
        layout.addWidget(self.status_label)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    @Slot()
    def __on_add_contact(self):
        """
        Handles the event when the Add Contact button is clicked.
        Adds a new contact to the table if both name and phone fields are populated.
        """
        # Extract input from the fields
        name = self.contact_name_input.text().strip()
        phone = self.phone_input.text().strip()

        # Check for valid input
        if name and phone:
            # Add a new row at the end of the table
            row_position = self.contact_table.rowCount()
            self.contact_table.insertRow(row_position)

            # Create QTableWidgetItem for each input and add to table
            name_item = QTableWidgetItem(name)
            phone_item = QTableWidgetItem(phone)
            self.contact_table.setItem(row_position, 0, name_item)
            self.contact_table.setItem(row_position, 1, phone_item)

            # Update status label
            self.status_label.setText(f"Added contact: {name}")
        else:
            # Prompt user to provide both fields
            self.status_label.setText("Please enter a contact name and phone number.")

    @Slot()
    def __on_remove_contact(self):
        """
        Handles the event when the Remove Contact button is clicked.
        Removes the selected contact from the table after confirmation.
        """
        # Get the selected row
        selected_row = self.contact_table.currentRow()

        # Confirm row selection
        if selected_row >= 0:
            # Show confirmation dialog
            reply = QMessageBox.question(
                self,
                "Remove Contact",
                "Are you sure you want to remove the selected contact?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            
            # Check the user's response
            if reply == QMessageBox.Yes:
                # Remove the selected row and update the status label
                self.contact_table.removeRow(selected_row)
                self.status_label.setText("Contact removed.")
            else:
                # Update the status label if the user clicks 'No'
                self.status_label.setText("Contact removal canceled.")
        else:
            # If no row is selected, prompt the user
            self.status_label.setText("Please select a row to be removed.")
