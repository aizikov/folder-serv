from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QLabel, QWidget, QListWidget, QPushButton, QInputDialog, QMessageBox
from file_manager_functions import FileManagerFunctions
# Импортируем класс с методами для работы с файлами
import os
from datetime import datetime

# Список вариантов сортировки
sort_items = ["Name", "Extension", "Modification Time"]

class FileManagerUI(QMainWindow):
    def __init__(self):
        super().__init__()
        # Устанавливаем заголовок окна
        self.setWindowTitle('File Manager')
        # Устанавливаем размеры окна
        self.setGeometry(100, 100, 400, 300)
        # Устанавливаем начальное значение маски
        self.mask = '*.*'
        # Устанавливаем начальное значение сортировки
        self.sort = sort_items[0]

        # Создаем вертикальный layout
        layout = QVBoxLayout()

        # Создаем метку для отображения текущей маски
        self.mask_label = QLabel(self.mask)

        # Создаем список для отображения файлов
        self.file_list = QListWidget()
        # Заполняем список файлами из директории
        self.populate_file_list()

         # Создаем кнопки для основных операций
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
        
        # Добавляем виджеты и кнопки на layout
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
        # Устанавливаем layout в качестве центрального виджета
        self.setCentralWidget(widget)

    def populate_file_list(self):
        # Метод для заполнения списка файлов из директории
        # Получаем отсортированный список файлов
        files = FileManagerFunctions.get_files_list(self.mask, self.sort)
        # Очищаем список
        self.file_list.clear()
        for file in files:
            # Добавляем каждый файл в список
            self.file_list.addItem(file)

    def delete_file(self):
        # Метод для удаления выбранного файла
        # Получаем выбранный файл из списка
        selected_item = self.file_list.currentItem().text()
        confirm_delete = QMessageBox.question(self, 
                                              'Confirm Delete', 
                                              f'Are you sure you want to delete {selected_item}?', 
                                              QMessageBox.Yes | QMessageBox.No)
        if confirm_delete == QMessageBox.Yes:
            # Удаляем файл
            FileManagerFunctions.delete_file(selected_item)
            # Обновляем список файлов
            self.populate_file_list()


    def create_empty_file(self):
        # Метод для создания пустого файла
        # Запрашиваем у пользователя имя файла
        file_name, ok_pressed = QInputDialog.getText(self, "Create Empty File", "Enter file name:")
        if ok_pressed and file_name:
            # Создаем пустой файл с указанным именем
            FileManagerFunctions.create_empty_file(file_name)
            self.file_list.clear()
            # Обновляем список файлов
            self.populate_file_list()

    def rename_file(self):
        # Метод для переименования файла
        # Получаем выбранный файл из списка
        selected_item = self.file_list.currentItem().text()
        # Запрашиваем у пользователя новое имя файла
        new_name, ok_pressed = QInputDialog.getText(self, "Rename File", f"Enter new name for {selected_item}:", text=selected_item)
        if ok_pressed and new_name:
            if new_name.endswith(".txt"):
                # Переименовываем файл
                FileManagerFunctions.rename_file(selected_item, new_name)
                # Обновляем список файлов
                self.populate_file_list()
            else:
                QMessageBox.warning(None, "Invalid Extension", "File can only be renamed with a .txt extension")

    def edit_file(self):
        # Метод для редактирования содержимого файла
        # Получаем выбранный файл из списка
        selected_item = self.file_list.currentItem().text()
        file_content = FileManagerFunctions.get_file_content(selected_item)

        # Запрашиваем у пользователя новое содержимое файла
        new_content, ok_pressed = QInputDialog.getMultiLineText(self, "Edit File", f"Edit {selected_item}:", file_content)
        if ok_pressed:
            # Редактируем файл
            FileManagerFunctions.edit_file(selected_item, new_content)

    def searh_file(self):
        # Метод для поиска файлов по маске
        # Запрашиваем у пользователя маску для поиска
        new_mask, ok_pressed = QInputDialog.getText(self, "Search mask", f"Enter mask:", text=self.mask)
        self.mask = new_mask
        self.mask_label.setText("Mask: " + self.mask)
        # Обновляем список файлов
        self.populate_file_list()
    
    def display_file_info(self):
        # Метод для отображения информации о выбранном файле
        selected_item = self.file_list.currentItem().text()
        # Получаем выбранный файл из списка
        file_path = FileManagerFunctions.get_file_path(selected_item)
        # Получаем полный путь к файлу
        file_size = os.path.getsize(file_path)
        creation_time = os.path.getctime(file_path)
        modification_time = os.path.getmtime(file_path)

        # Формируем информацию о файле
        creation_time_str = datetime.fromtimestamp(creation_time).strftime('%Y-%m-%d %H:%M:%S')
        # Отображаем информацию о файле в диалоговом окне
        modification_time_str = datetime.fromtimestamp(modification_time).strftime('%Y-%m-%d %H:%M:%S')

        info_message = f"File: {selected_item}\nSize: {file_size} bytes\nCreation Time: {creation_time_str}\nModification Time: {modification_time_str}"
        QMessageBox.information(self, "File Information", info_message)
    
    def open_sort_dialog(self):
        # Метод для открытия диалогового окна с выбором метода сортировки
        # Запрашиваем у пользователя метод сортировки
        item, ok_pressed = QInputDialog.getItem(self, "Sort by", "Select sorting type:", sort_items, 0, False)
        if ok_pressed and item:
            self.mask_label.setText("Mask: " + self.mask + ' Sort by: ' + item)
            # Устанавливаем новый метод сортировки
            self.sort = item
            # Обновляем список файлов
            self.populate_file_list()