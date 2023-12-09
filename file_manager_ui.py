from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QLabel, QWidget, QListWidget, QPushButton, QInputDialog, QMessageBox
from file_manager_functions import FileManagerFunctions
import os
from datetime import datetime

sort_items = ["Name", "Extension", "Modification Time"]

class FileManagerUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('File Manager')
        self.setGeometry(100, 100, 400, 300)
        self.mask = '*.*'
        self.sort = sort_items[0]

        layout = QVBoxLayout()

        self.mask_label = QLabel(self.mask)

        self.file_list = QListWidget()
        self.populate_file_list()

        self.delete_button = QPushButton('Delete')
        self.delete_button.clicked.connect(self.delete_file)

        self.create_button = QPushButton('Create Empty File')
        self.create_button.clicked.connect(self.create_empty_file)

        self.rename_button = QPushButton("Rename File")
        self.rename_button.clicked.connect(self.rename_file)

        self.edit_button = QPushButton("Edit File")
        self.edit_button.clicked.connect(self.edit_file)

        self.searh_button = QPushButton("Search Files")
        self.searh_button.clicked.connect(self.searh_file)

        self.info_button = QPushButton("info File")
        self.info_button.clicked.connect(self.display_file_info)

        self.sort_button = QPushButton("Sort Files")
        self.sort_button.clicked.connect(self.open_sort_dialog)
        
        layout.addWidget(self.mask_label)
        layout.addWidget(self.file_list)
        layout.addWidget(self.delete_button)
        layout.addWidget(self.create_button)
        layout.addWidget(self.rename_button)
        layout.addWidget(self.edit_button)
        layout.addWidget(self.searh_button)
        layout.addWidget(self.info_button)
        layout.addWidget(self.sort_button)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def populate_file_list(self):
        files = FileManagerFunctions.get_files_list(self.mask, self.sort)
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
        new_name, ok_pressed = QInputDialog.getText(self, "Rename File", f"Enter new name for {selected_item}:", text=selected_item)
        if ok_pressed and new_name:
            if new_name.endswith(".txt"):
                FileManagerFunctions.rename_file(selected_item, new_name)
                self.populate_file_list()
            else:
                QMessageBox.warning(None, "Invalid Extension", "File can only be renamed with a .txt extension")

    def edit_file(self):
        selected_item = self.file_list.currentItem().text()
        file_content = FileManagerFunctions.get_file_content(selected_item)

        new_content, ok_pressed = QInputDialog.getMultiLineText(self, "Edit File", f"Edit {selected_item}:", file_content)
        if ok_pressed:
            FileManagerFunctions.edit_file(selected_item, new_content)

    def searh_file(self):
        new_mask, ok_pressed = QInputDialog.getText(self, "Search mask", f"Enter mask:", text=self.mask)
        self.mask = new_mask
        self.mask_label.setText("Mask: " + self.mask)
        self.populate_file_list()
    
    def display_file_info(self):
        selected_item = self.file_list.currentItem().text()
        file_path = FileManagerFunctions.get_file_path(selected_item)
        file_size = os.path.getsize(file_path)
        creation_time = os.path.getctime(file_path)
        modification_time = os.path.getmtime(file_path)

        creation_time_str = datetime.fromtimestamp(creation_time).strftime('%Y-%m-%d %H:%M:%S')
        modification_time_str = datetime.fromtimestamp(modification_time).strftime('%Y-%m-%d %H:%M:%S')

        info_message = f"File: {selected_item}\nSize: {file_size} bytes\nCreation Time: {creation_time_str}\nModification Time: {modification_time_str}"
        QMessageBox.information(self, "File Information", info_message)
    
    def open_sort_dialog(self):
        item, ok_pressed = QInputDialog.getItem(self, "Sort by", "Select sorting type:", sort_items, 0, False)
        if ok_pressed and item:
            self.mask_label.setText("Mask: " + self.mask + ' Sort by: ' + item)
            self.sort = item
            self.populate_file_list()