import mysql.connector
import configparser
import os
from utils.logger import  Logger

config_location = ''

for currentpath, folders, files in os.walk('.'):
    for file in files:
        if file == 'config.txt':
            config_location = os.path.join(currentpath, file)

parser = configparser.ConfigParser()
parser.read(config_location)


class Database:

    def __init__(self):
        self.logger = Logger(self.__class__.__name__).get()
        self.logger.info("Attempting connect to database..")
        print('Connecting to database..')

        try:
            self.conn = mysql.connector.connect(
                host=parser.get("db-config", "host"),
                user=parser.get("db-config", "user"),
                password=parser.get("db-config", "password"),
                database=parser.get("db-config", "database")
            )

            self.logger.info("Connected to database..")
            print('Connected to database..')

            self.cursor = self.conn.cursor()
        except Exception as e:
            print("Can't connect to database..")
            self.logger.error("Connection not established..", e)

    def execute_query(self, sql):
        try:
            self.logger.info("Executing query..")
            self.cursor.execute(sql)
            self.logger.info("Query executed..")
            print("Table created successfully..")

        except Exception as e:
            print("Table creating error..")
            self.logger.error("Query not executed..", e)

    def commit_n_close(self):
        try:
            print("Connection closing..")
            self.logger.info("Connection closing..")

            self.conn.commit()
            self.conn.close()

            print("Connection closed..")
            self.logger.info("Connection closed..")
        except Exception as e:
            print("Error on connection close..")
            self.logger.error("Error on connection close..", e)

