import sys
from PyQt5.QtWidgets import QApplication
from file_manager_ui import FileManagerUI

if __name__ == '__main__':
    app = QApplication(sys.argv)
    file_manager = FileManagerUI()
    file_manager.show()
    sys.exit(app.exec_())