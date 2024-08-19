import sys
from PyQt5.QtWidgets import QApplication
from gui.main_window import MainWindow
from database.db_operations import DatabaseManager

def main():
    app = QApplication(sys.argv)
    db_manager = DatabaseManager("your_db_name", "your_username", "your_password")
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()