from utils.logger import Logger
from base.json_maker import JsonMaker
import os

supported_types = {
    'json': JsonMaker
}


class FormatSwitcher:

    def __init__(self, path):
        self.logger = Logger(self.__class__.__name__).get()

        self.is_file_existing(path)
        file_type = self.get_file_type(path)
        self.is_file_supported(file_type)

        self.process_maker(file_type, path)

    def process_maker(self, file_type, path):
        class_ref = supported_types.get(file_type)
        obj = class_ref(path)
        obj.process_data()

    def is_file_existing(self, path):
        if not os.path.exists(path):
            print("There is not file on that path")
            self.logger.warn("There is not file on that path")
            raise Exception('File not existing')

    def get_file_type(self, path):
        file_type = path.split(".", 1)[1]

        print(f'File type is {file_type}')
        self.logger.info(f'File type is {file_type}')

        return file_type

    def is_file_supported(self, file_type):
        if file_type in supported_types.keys():
            return True
        else:
            self.logger.error(f'Format {file_type} is not supported')
            raise Exception(f'Format {file_type} is not supported')
