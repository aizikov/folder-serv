from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QListWidget, QPushButton, QInputDialog, QMessageBox
from file_manager_functions import FileManagerFunctions

class FileManagerUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('File Manager')
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        self.file_list = QListWidget()
        self.populate_file_list()

        self.delete_button = QPushButton('Delete')
        self.delete_button.clicked.connect(self.delete_file)

        self.create_button = QPushButton('Create Empty File')
        self.create_button.clicked.connect(self.create_empty_file)

        self.rename_button = QPushButton("Rename File")
        self.rename_button.clicked.connect(self.rename_file)
        
        layout.addWidget(self.file_list)
        layout.addWidget(self.delete_button)
        layout.addWidget(self.create_button)
        layout.addWidget(self.rename_button)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def populate_file_list(self):
        files = FileManagerFunctions.get_files_list()
        self.file_list.clear()
        for file in files:
            self.file_list.addItem(file)

    def delete_file(self):
        selected_item = self.file_list.currentItem().text()
        confirm_delete = QMessageBox.question(self, 
                                              'Confirm Delete', 
                                              f'Are you sure you want to delete {selected_item}?', 
                                              QMessageBox.Yes | QMessageBox.No)
        if confirm_delete == QMessageBox.Yes:
            FileManagerFunctions.delete_file(selected_item)
            self.populate_file_list()


    def create_empty_file(self):
        file_name, ok_pressed = QInputDialog.getText(self, "Create Empty File", "Enter file name:")
        if ok_pressed and file_name:
            FileManagerFunctions.create_empty_file(file_name)
            self.file_list.clear()
            self.populate_file_list()

    def rename_file(self):
        selected_item = self.file_list.currentItem().text()
        new_name, ok_pressed = QInputDialog.getText(self, "Rename File", f"Enter new name for {selected_item}:")
        if ok_pressed and new_name:
            if new_name.endswith(".txt"):
                FileManagerFunctions.rename_file(selected_item, new_name)
                self.populate_file_list()
            else:
                QMessageBox.warning(None, "Invalid Extension", "File can only be renamed with a .txt extension")


    