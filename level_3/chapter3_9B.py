import sqlite3

class DatabaseConnection:
    def __init__(self, db_name):
        self.db_name = db_name
        self.connection = None

    def __enter__(self):
        self.connection = sqlite3.connect(self.db_name)
        print(f"Connected to database: {self.db_name}")
        return self.connection.cursor()

    def __exit__(self, exc_type, exc_value, exc_tb):
        if self.connection is not None:
            if exc_type:
                print(f"An exception occurred: {exc_value}. Rolling back transaction.")
                self.connection.rollback()
            else:
                print(f"No exception. Committing transaction.")
                self.connection.commit()

            self.connection.close()
            print(f"Closed connection")
    
        return False  # Propagate exception if any

# ---Usage Example 1: Successful Database Operations---
with DatabaseConnection(":memory:") as cursor:
    cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT)")
    cursor.execute("INSERT INTO users (name) VALUES (?)", ("Alice",))
    print()

# ---Usage Example 2: Exception Handling in Database Operations---
print("\n---Usage Example 2: Exception Handling in Database Operations---")
try:
    with DatabaseConnection(":memory:") as cursor:
        cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT)")
        # This SQL is intentionally incorrect to cause an error. Missing 'S' in 'VALUES'
        cursor.execute("INSERT INTO users (name) VALUE (?)", ("Bob",))
except sqlite3.OperationalError as e:
    print(f"Caught an exception: {e}")        