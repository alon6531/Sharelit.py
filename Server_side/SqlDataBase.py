import sqlite3
import hashlib

class SqlDataBase:
    def __init__(self, host='127.0.0.1', port=65432):
        db_name = 'users.db'
        # Initialize the server and database connection
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name, check_same_thread=False)
        self.cursor = self.conn.cursor()

        # Create or update the users table to include a balance column
        self.cursor.execute('''
                      CREATE TABLE IF NOT EXISTS users (
                          username TEXT PRIMARY KEY,
                          password TEXT,
                          first_name TEXT
                      )
                  ''')
        self.conn.commit()



    def check_credentials(self, username, password):
        """Check user credentials for login"""
        try:
            # ashing password
            password =hashlib.sha256((password + "daddy").encode('utf-8')).hexdigest()

            self.cursor.execute('SELECT * FROM users WHERE username=?', (username,))
            result = self.cursor.fetchone()
            if result:
                stored_password = result[1]  # Password stored as plain text
                if stored_password == password:
                    print("t")
                    return True
        except Exception as e:
            print(f"Error: {e}")
        return False

    def create_user(self, first_name, username, password):
        """Create a new user and insert into the database"""

        try:
            #ashing password
            password = hashlib.sha256((password + "daddy").encode('utf-8')).hexdigest()

            self.cursor.execute(
                'INSERT INTO users (first_name, username, password) VALUES (?, ?, ?)',
                (first_name, username, password)
            )
            self.conn.commit()
            print("User created successfully.")
            return True
        except sqlite3.IntegrityError:
            print(f"Error: A user with the email '{username}' already exists.")
            return False
        except Exception as e:
            print(f"Unexpected error while creating user: {e}")
            return False

    def print_all_users(self):
        """Print all users in the database, including their balance"""
        try:
            self.cursor.execute('SELECT * FROM users')
            rows = self.cursor.fetchall()
            if rows:
                print("Users in the database:")
                for row in rows:
                    print(f"First Name: {row[2]}, Username: {row[0]}, Password: {row[1]}")
            else:
                print("No users found in the database.")
        except Exception as e:
            print(f"Error retrieving users: {e}")


