import os
import fnmatch

# Устанавливаем директорию, в которой будем работать
directory = './docs/'

class FileManagerFunctions:
    @staticmethod
    def get_files_list(mask, sort):
        
        # Получаем список файлов в директории с помощью list comprehension и фильтруем их по расширению
        files = [f for f in os.listdir(directory) if f.endswith('.txt')]
        
        # Применяем маску к файлам с помощью fnmatch
        filtered_files = [file for file in files if fnmatch.fnmatch(file, mask)]

        # Сортируем файлы в зависимости от выбранного метода сортировки
        if sort == 'Extension':
            # Сортируем файлы по расширению
            filtered_files.sort(key=lambda x: x.split('.')[-1])
        
        elif sort == 'Modification Time':
            # Сортируем файлы по времени последнего изменения
            filtered_files.sort(key=lambda x: os.path.getmtime(os.path.join(directory, x)))

        else:
            # Сортируем файлы по имени
            filtered_files.sort()

        return filtered_files

    @staticmethod
    def delete_file(file_name):
        # Получаем полный путь к файлу
        file_path = directory + file_name

        # Удаляем файл
        os.remove(file_path)

    # Добавляем методы для создания, переименования и редактирования файлов

    @staticmethod
    def create_empty_file(file_name):
        # Формируем полный путь к новому файлу
        file_path = directory + file_name + '.txt'

        with open(file_path, 'w'):
            # Создаем новый файл
            pass

    @staticmethod
    def rename_file(file_name, new_name):
        # Получаем полный путь к старому файлу
        old_file_path = directory + file_name

        # Формируем полный путь к новому имени файла
        new_file_path = directory + new_name

        # Переименовываем файл
        os.rename(old_file_path, new_file_path)

    @staticmethod
    def get_file_content(file_name):
        # Получаем полный путь к файлу
        file_path = directory + file_name

        try:
            # Открываем файл для чтения
            with open(file_path, 'r') as file:
                # Читаем содержимое файла
                content = file.read()

                return content
            
        except FileNotFoundError:
            # Если файл не найден, возвращаем пустую строку
            return ''

    @staticmethod
    def edit_file(file_name, new_content):
        # Получаем полный путь к файлу
        file_path = directory + file_name

        try:
            # Открываем файл для записи
            with open(file_path, 'w') as file:
                # Записываем новое содержимое файла
                file.write(new_content)

        except FileNotFoundError:
            # Если файл не найден, возвращаем None
            return None
    
    @staticmethod
    def get_file_path(file_name):
        # Получаем полный путь к файлу
        file_path = directory + file_name
        
        # Возвращаем полный путь к файлу
        return file_path