from base.database import Database
from base.json_reader import JsonReader
from base.operations import Operations
from utils.logger import Logger


def validate_foreign_keys(row):
    is_valid = True

    for item in row:
        for key in item:
            if item[key] == '':
                is_valid = False

    return is_valid


def validate_data(row):
    is_valid = True

    for item in row:
        if "foreign_keys" in row:
            if row['foreign_keys'] is not None:
                is_valid = validate_foreign_keys(row['foreign_keys'])
            else:
                break

        if row[item] == '':
            is_valid = False

    return is_valid


class JsonMaker:

    def __init__(self, path):
        self.logger = Logger(self.__class__.__name__).get()
        self.db = Database()
        self.reader = JsonReader(path)
        self.operation = Operations()

    def get_data_from_json(self):
        print("Collecting data from json")
        self.logger.info("Collecting data from json")
        return self.reader.read()

    def process_row(self, row):
        table = row.get("table")
        columns = row.get("columns")
        primary_key = row.get("primary_key")
        foreign_keys = row.get("foreign_keys")

        query = self.operation.create_query(table, columns, primary_key, foreign_keys)

        self.db.execute_query(query)

    def process_data(self):
        data = self.get_data_from_json()
        if isinstance(data, dict):
            is_data_valid = validate_data(data)
            if is_data_valid:
                print("Processing data")
                self.logger.info("Processing data")
                self.process_row(data)
            else:
                print("Records not valid")
                self.logger.warn("Records not valid")

        if isinstance(data, list):
            for item in data:
                is_data_valid = validate_data(item)
                if is_data_valid:
                    print("Processing data")
                    self.logger.info("Processing data")
                    self.process_row(item)
                else:
                    print("Records not valid")
                    self.logger.warn("Records not valid")

        self.db.commit_n_close()
