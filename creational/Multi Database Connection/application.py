from DatabaseFactory import SQLDatabaseFactory, NoSQLDatabaseFactory

def application():
    print("Application started")

    # MySQL Connection
    sql_database_factory = SQLDatabaseFactory()
    # mysql_connection = sql_database_factory.create_connection("MySQL", "localhost", 3306, "root", "password", "database_name")
    # mysql_connection.connect()
    # mysql_connection.execute("CREATE TABLE users (id INT, name VARCHAR(255))")
    # mysql_connection.execute("INSERT INTO users (id, name) VALUES (1, 'John')")
    # mysql_connection.execute("INSERT INTO users (id, name) VALUES (2, 'Jane')")
    # mysql_connection.execute("INSERT INTO users (id, name) VALUES (3, 'Jim')")
    # mysql_connection.execute("INSERT INTO users (id, name) VALUES (4, 'Jill')")
    # mysql_connection.execute("INSERT INTO users (id, name) VALUES (5, 'Jack')")
    # mysql_connection.execute("INSERT INTO users (id, name) VALUES (6, 'Jill')")
    # mysql_connection.execute("INSERT INTO users (id, name) VALUES (7, 'Jack')")
    # mysql_connection.execute("INSERT INTO users (id, name) VALUES (8, 'Jill')")
    # mysql_connection.execute("INSERT INTO users (id, name) VALUES (9, 'Jack')")
    # mysql_connection.execute("INSERT INTO users (id, name) VALUES (10, 'Jill')")
    # results = mysql_connection.fetch("SELECT * FROM users")
    # print(results)
    # mysql_connection.disconnect()


    # PostgreSQL Connection

    # postgres_connection = sql_database_factory.create_connection("PostgreSQL", "localhost", 5432, "root", "password", "database_name")
    # postgres_connection.connect()
    # postgres_connection.execute("CREATE TABLE users (id INT, first_name VARCHAR(255), last_name VARCHAR(255))")
    # postgres_connection.execute("INSERT INTO users (id, first_name, last_name) VALUES (1, 'Mohab', 'El-Haj')")
    # postgres_connection.execute("INSERT INTO users (id, first_name, last_name) VALUES (2, 'Ahmed', 'Fawzy')")
    # postgres_connection.execute("INSERT INTO users (id, first_name, last_name) VALUES (3, 'Mohamed', 'Ali')")
    # postgres_connection.execute("INSERT INTO users (id, first_name, last_name) VALUES (4, 'Youssef', 'Ahmed')")
    # postgres_connection.execute("INSERT INTO users (id, first_name, last_name) VALUES (5, 'Omar', 'Mostafa')")
    # postgres_connection.execute("INSERT INTO users (id, first_name, last_name) VALUES (6, 'Fathy', 'Saad')")
    # results = postgres_connection.fetch("SELECT * FROM users")
    # print(results)
    # postgres_connection.disconnect()

    no_sql_database_factory = NoSQLDatabaseFactory()

    # MongoDB Connection
    mongodb_connection = no_sql_database_factory.create_connection("MongoDB", "localhost", 27017, "root", "password", "users")
    mongodb_connection.connect()
    mongodb_connection.execute("db.createCollection('users')")
    mongodb_connection.execute("db.users.insertOne({id: 1, name: 'John'})")
    mongodb_connection.execute("db.users.insertOne({id: 2, name: 'Jane'})")
    mongodb_connection.execute("db.users.insertOne({id: 3, name: 'Jim'})")
    mongodb_connection.execute("db.users.insertOne({id: 4, name: 'Jill'})")
    mongodb_connection.execute("db.users.insertOne({id: 5, name: 'Jack'})")
    mongodb_connection.execute("db.users.insertOne({id: 6, name: 'Jill'})")
    mongodb_connection.execute("db.users.insertOne({id: 7, name: 'Jack'})")
    mongodb_connection.execute("db.users.insertOne({id: 8, name: 'Jill'})")
    mongodb_connection.execute("db.users.insertOne({id: 9, name: 'Jack'})")
    results = mongodb_connection.execute("db.users.find({})")
    print(results)
    mongodb_connection.disconnect()


if __name__ == "__main__":
    application()
