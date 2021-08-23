import json
import os


class Reader:

    def __init__(self, path):

        if not os.path.exists(path):
            print("There is not file on that path.")

        if path.split(".", 1)[1] != 'json':
            print("File format must be json.")

        try:
            self.file = open(path)
        except:
            print("Can't open file.")

    def read(self):
        output = json.load(self.file)
        self.file.close()
        return output

    