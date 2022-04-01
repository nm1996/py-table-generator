import json
import os
from utils.logger import Logger


class Reader:

    def __init__(self, path):
        self.logger = Logger(self.__class__.__name__).get()

        if not os.path.exists(path):
            print("There is not file on that path..")
            self.logger.warn("There is not file on that path..")

        if path.split(".", 1)[1] != 'json':
            print("File format must be json..")
            self.logger.warn("File format must be json..")

        try:
            self.file = open(path)
        except Exception as e:
            print("Can't open file..")
            self.logger.error("Can't open file..", e)

    def read(self):
        print("Loading json file..")
        self.logger.info("Loading json file..")
        self.logger.info("Reading json file..")
        output = json.load(self.file)

        self.logger.info("Closing json file..")
        print("Closing json file..")
        self.file.close()

        return output

    