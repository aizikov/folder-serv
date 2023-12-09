import os
import fnmatch

directory = './docs/'

class FileManagerFunctions:
    @staticmethod
    def get_files_list(mask, sort):
        files = [f for f in os.listdir(directory) if f.endswith('.txt')]
        filtered_files = [file for file in files if fnmatch.fnmatch(file, mask)]

        if sort == 'Extension':
            filtered_files.sort(key=lambda x: x.split('.')[-1])  # Sort the files by extension
        elif sort == 'Modification Time':
            filtered_files.sort(key=lambda x: os.path.getmtime(os.path.join(directory, x)))  # Sort the files by modification time
        else:
            filtered_files.sort()  # Sort the files by name
        return filtered_files

    @staticmethod
    def delete_file(file_name):
        file_path = directory + file_name
        os.remove(file_path)

    # Добавьте методы для создания, переименования и редактирования файлов

    @staticmethod
    def create_empty_file(file_name):
        file_path = directory + file_name + '.txt'
        with open(file_path, 'w'):
            pass

    @staticmethod
    def rename_file(file_name, new_name):
        old_file_path = directory + file_name
        new_file_path = directory + new_name
        os.rename(old_file_path, new_file_path)

    @staticmethod
    def get_file_content(file_name):
        file_path = directory + file_name
        try:
            with open(file_path, 'r') as file:
                content = file.read()
                return content
        except FileNotFoundError:
            return ''

    @staticmethod
    def edit_file(file_name, new_content):
        file_path = directory + file_name
        try:
            with open(file_path, 'w') as file:
                file.write(new_content)
        except FileNotFoundError:
            return None
    
    @staticmethod
    def get_file_path(file_name):
        file_path = directory + file_name
        return file_path