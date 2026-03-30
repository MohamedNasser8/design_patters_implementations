from abc import ABC
from abc import abstractmethod
import mysql.connector
import psycopg2

class DatabaseConnection(ABC):
    def __init__(self, host, port, username, password, database_name):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.database_name = database_name
        self.connection = None
        self.cursor = None

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def disconnect(self):
        pass

    @abstractmethod
    def execute(self, query):
        pass

    @abstractmethod
    def fetch(self, query):
        pass

class SQLDatabaseConnection(DatabaseConnection):
    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def disconnect(self):
        pass

    def execute(self, query):
        print(f"Executing query: {query}")
        self.cursor.execute(query)
        self.connection.commit()

    def fetch(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchall()
        


class MySQLConnection(SQLDatabaseConnection):
    def connect(self):
        self.connection = mysql.connector.connect(
            host=self.host,
            port=self.port,
            user=self.username,
            password=self.password,
            database=self.database_name
        )
        self.cursor = self.connection.cursor()

    def disconnect(self):
        self.cursor.close()
        self.connection.close()


class PostgreSQLConnection(SQLDatabaseConnection):
    def connect(self):
        self.connection = psycopg2.connect(
            host=self.host,
            port=self.port,
            user=self.username,
            password=self.password,
            database=self.database_name
        )
        self.cursor = self.connection.cursor()

    def disconnect(self):
        self.cursor.close()
        self.connection.close()


class RedisConnection(DatabaseConnection):
    def connect(self):
        pass

    def disconnect(self):
        pass

    def execute(self, query):
        pass


class MongoDBConnection(DatabaseConnection):
    def connect(self):
        pass

    def disconnect(self):
        pass

    def execute(self, query):
        pass