import mysql.connector
import configparser

parser = configparser.ConfigParser()
parser.read("config.txt")


class Database:

    def __init__(self):
        self.conn = mysql.connector.connect(
            host=parser.get("db-config", "host"),
            user=parser.get("db-config", "user"),
            password=parser.get("db-config", "password"),
            database=parser.get("db-config", "database")
        )
        self.cursor = self.conn.cursor()

    def executeQuery(self, sql):
        self.cursor.execute(sql)
        print("Table created successfully")

    def commitAndClose(self):
        self.conn.commit()
        self.conn.close()

    def createQuery(self, table, columns, primary_key, foreign_keys=None):

        sql = ""
        columnsString = self.generateColumnsString(columns)

        if foreign_keys == None:
            sql = self.sqlWithoutForeignKeys(table, columnsString, primary_key)

        if foreign_keys != None:
            keysString = self.generateKeysString(foreign_keys)
            sql = self.sqlWithForeignKeys(
                table, columnsString, primary_key, keysString)

        return sql

    def sqlWithoutForeignKeys(self, table, columnsString, primary_key):
        return "CREATE TABLE IF NOT EXISTS " + table + \
            "("+columnsString+"PRIMARY KEY ("+primary_key+"))"

    def sqlWithForeignKeys(self, table, columnsString, primary_key, keysString):
        return "CREATE TABLE IF NOT EXISTS " + table + \
            "("+columnsString+"PRIMARY KEY ("+primary_key+"),"+keysString+")"

    def generateColumnsString(self, columns):
        columnsString = ""
        for item in columns:
            columnsString += item + " " + columns[item] + ", "
        return columnsString

    def generateKeysString(self, foreign_keys):
        keysString = ""
        for item in foreign_keys:
            keysString += " FOREIGN KEY ("+item["id"]+") REFERENCES " + \
                item["table"]+"("+item["primary_key"]+"),"

        return keysString.removesuffix(',')
