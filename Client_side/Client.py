import socket
import json
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization
from Client_side import Engine
from Client_side.App.User import User
import threading


class Client:
    def __init__(self, server_host='127.0.0.1', tcp_port=65432, udp_port=12345):
        """
        Initialize the Client by generating keys, connecting to the server,
        and starting the application engine.
        """
        self.server_host = server_host
        self.tcp_port = tcp_port
        self.udp_port = udp_port

        # Generate RSA keys
        self.private_key, self.public_key = self.make_keys()
        self.public_key_pem = self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

        # Create TCP socket
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client_socket.connect((server_host, tcp_port))
            print(f"Connected to server at {server_host}:{tcp_port}")

            self.client_socket.send(self.public_key_pem)
            public_server_key_pem = self.client_socket.recv(1024)
            self.public_server_key = load_pem_public_key(public_server_key_pem)

            self.username = None
        except Exception as e:
            print(f"Failed to connect to server: {e}")
            self.client_socket.close()
            raise

        # Create UDP socket
        try:
            self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            print(f"UDP server listening on {server_host}:{udp_port}...")
        except Exception as e:
            print(f"Failed to connect to server: {e}")
            self.udp_socket.close()
            raise
        # Start UDP server listener in a separate thread
        self.udp_listener_thread = threading.Thread(target=self.listen_udp)
        self.udp_listener_thread.daemon = True
        self.udp_listener_thread.start()

        # Initialize the application engine
        self.app_engine = Engine.AppEngine(self)

    def make_keys(self):
        private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        public_key = private_key.public_key()
        return private_key, public_key

    def encrypt(self, text):
        return self.public_server_key.encrypt(
            text.encode(),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

    def listen_udp(self):
        """
        Listen for incoming UDP messages (server-side communication).
        """
        try:
            # Set socket option for address reuse
            self.udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

            self.udp_socket.bind((self.server_host, self.udp_port))
            print(f"UDP server listening on {self.server_host}:{self.udp_port}")

            while True:
                try:
                    data, addr = self.udp_socket.recvfrom(4096)
                    print(f"Received message from {addr}: {data.decode('utf-8')}")
                    # You can add custom handling of different message types here.
                    # For example, handling specific requests like game data, player updates, etc.

                except Exception as e:
                    print(f"Error receiving UDP message: {e}")
        except Exception as e:
            print(f"Error binding UDP socket: {e}")

    def log_in(self, login_username, login_password):
        try:
            self.client_socket.send(b'login')
            credentials = f"{login_username},{login_password}"
            self.client_socket.send(self.encrypt(credentials))
            response = self.client_socket.recv(1024).decode('utf-8')
            if response == 'True':
                print("Login successful!")
                self.username = login_username
                return True
            else:
                print("Login failed!")
                return False
        except Exception as e:
            print(f"Error during login: {e}")
            return False

    def register(self, user_name, username, password):
        try:
            self.client_socket.send(b'register')
            user_data = f"{user_name},{username},{password}"
            self.client_socket.send(self.encrypt(user_data))
            response = self.client_socket.recv(1024).decode('utf-8')
            print(response)
        except Exception as e:
            print(f"Error during registration: {e}")

    def receive_stories(self):
        try:
            self.client_socket.send(b'receive_stories')
            self.udp_socket.sendto(b'receive_stories_acr', (self.server_host, self.udp_port))
            data, _ = self.udp_socket.recvfrom(4096)
            json_data = data.decode('utf-8')
            stories_data = json.loads(json_data)

            # Extract data into arrays
            titles = stories_data['titles']
            contents = stories_data['contents']
            usernames = stories_data['usernames']
            pos_x = stories_data['pos_x']
            pos_y = stories_data['pos_y']

            # Print or return the arrays as needed
            print("Received titles:", titles)
            print("Received contents:", contents)
            print("Received usernames:", usernames)
            print("Received pos_x:", pos_x)
            print("Received pos_y:", pos_y)

            # Return the extracted data as arrays
            return titles, contents, usernames, pos_x, pos_y
        except Exception as e:
            print(f"Error receiving stories: {e}")
            return []

    def update_player(self, pos_x, pos_y):
        try:
            self.client_socket.send(b'update_player')

            data = {
                'username': self.username,
                'pos_x': pos_x,
                'pos_y': pos_y
            }
            json_data = json.dumps(data)
            print("Updating player")
            self.udp_socket.sendto(json_data.encode(), (self.server_host, self.udp_port))
        except Exception as e:
            print(f"Error updating player position: {e}")

    def receive_all_players(self):
        try:
            # Send request to the server for all players' data
            self.client_socket.send(b'send_all_players')
            self.udp_socket.sendto(b'receive_all_players_acr', (self.server_host, self.udp_port))
            # Receive response data from the server
            data, _ = self.udp_socket.recvfrom(4096)  # Receiving data from the server
            print("Received data:", data)  # Debugging line to see the raw data
            players_data = json.loads(data.decode('utf-8'))

            # Extract the number of players and their data
            num_players = players_data["num_players"]
            users = [User(p["username"], p["pos_x"], p["pos_y"]) for p in players_data["players"]]

            return num_players, users
        except Exception as e:
            print(f"Error receiving players' data: {e}")
            return 0, []

    def logout(self):
        try:
            self.client_socket.send(b'logout')
            self.client_socket.send(self.username.encode('utf-8'))
            response = self.client_socket.recv(1024).decode('utf-8')
            print(response)
        except Exception as e:
            print(f"Error during logout: {e}")
        finally:
            self.client_socket.close()
            print("Disconnected from server.")

    def get_user(self):
        return self.username

    def add_story(self, title, content, username, pos_x, pos_y):
        try:
            self.client_socket.send(b'add_story')
            self.client_socket.send(title.encode())
            self.client_socket.recv(1024)
            self.client_socket.send(content.encode())
            self.client_socket.recv(1024)
            self.client_socket.send(username.encode())
            self.client_socket.recv(1024)
            self.client_socket.send(str(pos_x).encode())
            self.client_socket.recv(1024)
            self.client_socket.send(str(pos_y).encode())
            response = self.client_socket.recv(1024).decode('utf-8')
            print(response)
        except Exception as e:
            print(f"Error adding story: {e}")


# Main entry point
if __name__ == "__main__":
    try:
        client = Client()
    except Exception as e:
        print(f"Client failed to start: {e}")
