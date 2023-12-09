import os

directory = './docs/'

class FileManagerFunctions:
    @staticmethod
    def get_files_list():
        
        files = [f for f in os.listdir(directory) if f.endswith('.txt')]
        return files

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