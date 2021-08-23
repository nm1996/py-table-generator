from database import Database
from reader import Reader


class Maker:

    def __init__(self, path):
        self.db = Database()
        self.reader = Reader(path)

    def getDataFromJson(self):
        return self.reader.read()

    def processRow(self, row):
        table = row.get("table")
        columns = row.get("columns")
        primary_key = row.get("primary_key")
        foreign_keys = row.get("foreign_keys")

        query = self.db.createQuery(table, columns, primary_key, foreign_keys)

        try:
            self.db.executeQuery(query)
        except:
            print("There is error")

    def processData(self):
        data = self.getDataFromJson()
        if isinstance(data, dict):
            isDataValid = self.validateData(data)
            if isDataValid:
                self.processRow(data)
            else:
                print("Records not valid")

        if isinstance(data, list):
            for item in data:
                isDataValid = self.validateData(item)
                if isDataValid:
                    self.processRow(item)
                else:
                    print("Records not valid")

    def validateData(self, row):
        isValid = True

        for item in row:
            if "foreign_keys" in row:
                if row['foreign_keys'] != None:
                    isValid = self.validateForeignKeys(row['foreign_keys'])
                else:
                    break

            if row[item] == '':
                isValid = False

        return isValid

    def validateForeignKeys(self, row):
        isValid = True

        for item in row:
            for key in item:
                if item[key] == '':
                    isValid = False

        return isValid
