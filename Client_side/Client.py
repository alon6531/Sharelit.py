import socket
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization
from Client_side import Engine
from Client_side.App.User import User
import json

class Client:
    def __init__(self, server_host='192.168.1.217', server_port=65432):
        """
        Initialize the Client by generating keys, connecting to the server,
        and starting the application engine.
        """
        # Generate RSA keys (private and public)
        self.private_key, self.public_key = self.make_keys()

        # Serialize the public key for sending to the server
        self.public_key_pem = self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

        # Create a socket and attempt to connect to the server
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client_socket.connect((server_host, server_port))
            print(f"Connected to server at {server_host}:{server_port}")

            # Send public key to the server and receive server's public key
            self.client_socket.send(self.public_key_pem)
            public_server_key_pem = self.client_socket.recv(1024)
            self.public_server_key = load_pem_public_key(public_server_key_pem)

            # Initialize username (to be set during login)
            self.username = None

        except Exception as e:
            print(f"Failed to connect to server: {e}")
            self.client_socket.close()
            raise

        # Initialize the application engine (handles UI interaction)
        self.app_engine = Engine.AppEngine(self)

    def make_keys(self):
        """
        Generate a new RSA key pair (private and public).
        """
        private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        public_key = private_key.public_key()
        return private_key, public_key

    def encrypt(self, text):
        """
        Encrypt the provided text using the server's public key and OAEP padding.
        """
        return self.public_server_key.encrypt(
            text.encode(),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

    def log_in(self, login_username, login_password):
        """
        Handle user login by sending credentials and receiving response from the server.
        """
        try:
            self.client_socket.send(b'login')
            credentials = f"{login_username},{login_password}"
            self.client_socket.send(self.encrypt(credentials))  # Encrypt credentials

            response = self.client_socket.recv(1024).decode('utf-8')
            if response == 'True':
                print("Login successful!")
                self.username = login_username  # Set the username after successful login
                return True
            else:
                print("Login failed!")
                return False
        except Exception as e:
            print(f"Error during login: {e}")
            return False

    def register(self, user_name, username, password):
        """
        Handle user registration by sending the user's details to the server.
        """
        try:
            self.client_socket.send(b'register')
            user_data = f"{user_name},{username},{password}"
            self.client_socket.send(self.encrypt(user_data))  # Encrypt user data

            response = self.client_socket.recv(1024).decode('utf-8')
            print(response)
        except Exception as e:
            print(f"Error during registration: {e}")

    def receive_stories(self):
        """
        Request stories from the server and process them, including positions.
        """
        try:
            self.client_socket.send(b'receive_stories')

            # Receive the number of stories and ensure it's a valid integer
            response = self.client_socket.recv(1024).decode('utf-8')
            try:
                data_count = int(response)
            except ValueError:
                print(f"Error: Expected an integer but received: {response}")
                return []

            titles, contents, usernames, x_positions, y_positions = [], [], [], [], []

            # Process stories
            for _ in range(data_count):
                title = self.client_socket.recv(1024).decode('utf-8')
                self.client_socket.send(b'receive')
                titles.append(title)

            for _ in range(data_count):
                content = self.client_socket.recv(1024).decode('utf-8')
                self.client_socket.send(b'receive')
                contents.append(content)

            for _ in range(data_count):
                username = self.client_socket.recv(1024).decode('utf-8')
                self.client_socket.send(b'receive')
                usernames.append(username)

            for _ in range(data_count):
                pos_x = int(self.client_socket.recv(1024).decode('utf-8'))  # Receive pos_x
                self.client_socket.send(b'receive')
                x_positions.append(pos_x)  # Store pos_x separately

            for _ in range(data_count):
                pos_y = int(self.client_socket.recv(1024).decode('utf-8'))  # Receive pos_y
                self.client_socket.send(b'receive')
                y_positions.append(pos_y)  # Store pos_y separately

            print("Received Titles:", titles)
            print("Received Contents:", contents)
            print("Received Usernames:", usernames)
            print("Received X Positions:", x_positions)
            print("Received Y Positions:", y_positions)

            return titles, contents, usernames, x_positions, y_positions
        except Exception as e:
            print(f"Error receiving stories: {e}")

    def logout(self):
        """
        Send logout request with the player's username and disconnect from the server.
        """
        try:
            # Send 'logout' action to the server
            self.client_socket.send(b'logout')

            # Send the username of the player logging out
            self.client_socket.send(self.username.encode('utf-8'))

            # Receive the server's response after logout action
            response = self.client_socket.recv(1024).decode('utf-8')
            print(response)  # Print server's response

        except Exception as e:
            print(f"Error during logout: {e}")

        finally:
            # Close the socket connection after the logout process
            self.client_socket.close()
            print("Disconnected from server.")

    def get_user(self):
        """
        Return the current username of the logged-in user.
        """
        return self.username

    def add_story(self, title, content, username, pos_x, pos_y):
        """
        Send a request to add a new story to the server, including position data.
        """
        try:
            self.client_socket.send(b'add_story')
            self.client_socket.send(title.encode())  # Send story title
            self.client_socket.recv(1024)  # Receive acknowledgment
            self.client_socket.send(content.encode())  # Send story content
            self.client_socket.recv(1024)  # Receive acknowledgment
            self.client_socket.send(username.encode())  # Send username
            self.client_socket.recv(1024)  # Receive acknowledgment
            self.client_socket.send(str(pos_x).encode())  # Send pos_x
            self.client_socket.recv(1024)  # Receive acknowledgment
            self.client_socket.send(str(pos_y).encode())  # Send pos_y
            response = self.client_socket.recv(1024).decode('utf-8')
            print(response)
        except Exception as e:
            print(f"Error adding story: {e}")

    def update_player(self, pos_x, pos_y):
        """
        Send the username and its position (x, y) to the server using JSON for faster communication.
        First, send a simple action message to the server, then the actual data.
        """
        try:
            # Send an initial action to the server to indicate we are updating player info
            self.client_socket.send(b'update_player')

            # Create a dictionary with the necessary data
            data = {
                'username': self.username,
                'pos_x': int(pos_x),
                'pos_y': int(pos_y)
            }

            # Convert the dictionary to a JSON string
            json_data = json.dumps(data)

            # Send the JSON data to the server
            self.client_socket.send(json_data.encode())

            # Receive response from server
            response = self.client_socket.recv(1024).decode('utf-8')
            print(response)

        except Exception as e:
            print(f"Error sending username and position: {e}")



    def receive_all_players(self):
        """
        Receive all players' information from the server in a more efficient way.
        """
        try:
            self.client_socket.send(b'send_all_players')

            # Get the full response in one recv call
            data = self.client_socket.recv(4096).decode('utf-8')

            # Parse JSON format
            players_data = json.loads(data)

            num_players = players_data["num_players"]
            users = [User(p["username"], p["pos_x"], p["pos_y"]) for p in players_data["players"]]

            return num_players, users

        except Exception as e:
            print(f"Error receiving players' data: {e}")
            return 0, []


# Main entry point
if __name__ == "__main__":
    try:
        client = Client()  # Create and start the client
    except Exception as e:
        print(f"Client failed to start: {e}")