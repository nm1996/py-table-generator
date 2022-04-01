class Operations:

    def __init__(self):
        pass

    def sql_with_foreign_keys(self, table, columns_string, primary_key, keys_string):
        return "CREATE TABLE IF NOT EXISTS " + table + \
               "(" + columns_string + "PRIMARY KEY (" + primary_key + ")," + keys_string + ")"

    def generate_columns_string(self, columns):
        columns_string = ""
        for item in columns:
            columns_string += item + " " + columns[item] + ", "
        return columns_string

    def sql_without_foreign_keys(self, table, columns_string, primary_key):
        return "CREATE TABLE IF NOT EXISTS " + table + \
               "(" + columns_string + "PRIMARY KEY (" + primary_key + "))"

    def generate_keys_string(self, foreign_keys):
        keys_string = ""
        for item in foreign_keys:
            keys_string += " FOREIGN KEY (" + item["id"] + ") REFERENCES " + \
                           item["table"] + "(" + item["primary_key"] + "),"

        return keys_string.removesuffix(',')

    def create_query(self, table, columns, primary_key, foreign_keys=None):

        sql = ""
        columns_string = self.generate_columns_string(columns)

        if foreign_keys is None:
            sql = self.sql_without_foreign_keys(table, columns_string, primary_key)

        if foreign_keys is not None:
            keys_string = self.generate_keys_string(foreign_keys)
            sql = self.sql_with_foreign_keys(
                table, columns_string, primary_key, keys_string)

        return sql
