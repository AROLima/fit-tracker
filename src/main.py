import sys
from PyQt5.QtWidgets import QApplication
from gui.main_window import MainWindow
from database.db_operations import DatabaseManager

def main():
    app = QApplication(sys.argv)
    db_manager = DatabaseManager("alunos", "postgres", "546375")
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()