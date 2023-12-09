import sys
from PyQt5.QtWidgets import QApplication
from file_manager_ui import FileManagerUI

if __name__ == '__main__':
    # Создаем экземпляр приложения
    app = QApplication(sys.argv)
    # Создаем экземпляр интерфейса файлового менеджера
    file_manager = FileManagerUI()
    # Отображаем интерфейс файлового менеджера
    file_manager.show()
    # Запускаем цикл обработки событий приложения
    sys.exit(app.exec_())