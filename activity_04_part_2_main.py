""""
Description: A client program written to verify correctness of 
the activity classes.
Author: ACE Faculty
Edited by: {Student Name}
Date: {Date}
"""
# REQUIREMENT - add import statements
from to_do_list.to_do_list import ToDoList

# GIVEN:
from PySide6.QtWidgets import QApplication

# GIVEN:
if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    mainWindow = ToDoList()
    mainWindow.show()
    sys.exit(app.exec())