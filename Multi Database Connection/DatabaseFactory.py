from abc import ABC
from abc import abstractmethod
from DatabaseConnection import MySQLConnection, PostgreSQLConnection, MongoDBConnection, RedisConnection

class DatabaseFactory(ABC):

    @abstractmethod
    def create_connection(self, database_type):
        pass

class SQLDatabaseFactory(DatabaseFactory):
    def create_connection(self, database_type, host, port, username, password, database_name):
        if database_type == "MySQL":
            return MySQLConnection(host, port, username, password, database_name)
        elif database_type == "PostgreSQL":
            return PostgreSQLConnection(host, port, username, password, database_name)
        else:
            raise ValueError(f"Invalid database type: {database_type}")

class NoSQLDatabaseFactory(DatabaseFactory):
    def create_connection(self, database_type, host, port, username, password, database_name):
        if database_type == "MongoDB":
            return MongoDBConnection()
        elif database_type == "Redis":
            return RedisConnection()
        else:
            raise ValueError(f"Invalid database type: {database_type}")