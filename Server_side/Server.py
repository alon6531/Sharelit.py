import socket
import threading
import json
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from Server_side import SqlDataBase, jsonDataBase
from Client_side.App.User import User


class Server:
    def __init__(self, host='192.168.1.217', port=65432):
        """
        Initialize the UDP Server, generate keys, and start listening.
        """
        self.sql_data_base = SqlDataBase.SqlDataBase()
        self.json_data_base = jsonDataBase.jsonDataBase()
        self.host = host
        self.port = port
        self.players = []

        # Generate RSA keys
        self.private_key, self.public_key = self.make_keys()
        self.public_key_pem = self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

        # Set up the UDP socket
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_socket.bind((self.host, self.port))

        print(f"UDP Server listening on {self.host}:{self.port}...")
        self.listen_for_clients()

    def make_keys(self):
        """ Generate a new RSA key pair. """
        private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        public_key = private_key.public_key()
        return private_key, public_key

    def decrypt(self, encrypted_text):
        """ Decrypt the encrypted message using the private key. """
        return self.private_key.decrypt(
            encrypted_text,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

    def listen_for_clients(self):
        """ Continuously listen for incoming UDP messages. """
        while True:
            try:
                data, client_address = self.server_socket.recvfrom(4096)
                threading.Thread(target=self.handle_client, args=(data, client_address)).start()
            except Exception as e:
                print(f"Error receiving data: {e}")

    def handle_client(self, data, client_address):
        """ Process received data and respond accordingly. """
        try:
            message = data.decode('utf-8')
            print(f"Received from {client_address}: {message}")

            if message == 'login':
                self.handle_login(client_address)

            elif message == 'receive_stories':
                self.handle_receive_stories(client_address)

            elif message == 'register':
                self.handle_register(client_address)

            elif message == 'add_story':
                self.handle_add_story(client_address)

            elif message == 'update_player':
                self.update_player(client_address)

            elif message == 'send_all_players':
                self.send_all_players(client_address)

            elif message == 'logout':
                self.handle_logout(client_address)

        except Exception as e:
            print(f"Error handling client {client_address}: {e}")

    def send_udp(self, message, client_address):
        """ Send a UDP message to the client. """
        self.server_socket.sendto(message.encode('utf-8'), client_address)

    def handle_login(self, client_address):
        """ Handle login by receiving credentials. """
        try:
            data, _ = self.server_socket.recvfrom(1024)
            credentials = self.decrypt(data).decode()
            username, password = credentials.split(',')
            print(f"Login attempt for {username}")

            if self.sql_data_base.check_credentials(username, password):
                self.send_udp("True", client_address)
            else:
                self.send_udp("False", client_address)
        except Exception as e:
            print(f"Error in login: {e}")
            self.send_udp("Error in login", client_address)

    def handle_receive_stories(self, client_address):
        """ Send stored stories to the client. """
        try:
            titles, contents, usernames, pos_x, pos_y = self.json_data_base.receive_data()

            stories_data = json.dumps({
                "titles": titles,
                "contents": contents,
                "usernames": usernames,
                "positions": list(zip(pos_x, pos_y))
            })

            self.send_udp(stories_data, client_address)
            print(f"Stories sent to {client_address}")
        except Exception as e:
            print(f"Error sending stories: {e}")
            self.send_udp("Error sending stories", client_address)

    def handle_register(self, client_address):
        """ Handle user registration. """
        try:
            data, _ = self.server_socket.recvfrom(1024)
            user_data = self.decrypt(data).decode()
            first_name, username, password = user_data.split(',')
            print(f"Registering user {username}")

            if self.sql_data_base.create_user(first_name, username, password):
                self.send_udp("Registration successful", client_address)
            else:
                self.send_udp("Registration failed", client_address)
        except Exception as e:
            print(f"Error in registration: {e}")
            self.send_udp("Error in registration", client_address)

    def handle_add_story(self, client_address):
        """ Handle adding a new story. """
        try:
            data, _ = self.server_socket.recvfrom(4096)
            story_data = json.loads(data.decode('utf-8'))

            title = story_data["title"]
            content = story_data["content"]
            username = story_data["username"]
            pos_x = story_data["pos_x"]
            pos_y = story_data["pos_y"]

            self.json_data_base.add_entry(title, content, username, pos_x, pos_y)
            self.send_udp("Story added successfully", client_address)
        except Exception as e:
            print(f"Error adding story: {e}")
            self.send_udp("Error adding story", client_address)

    def update_player(self, client_address):
        """ Update player's position. """
        try:
            data, _ = self.server_socket.recvfrom(1024)
            player_data = json.loads(data.decode('utf-8'))

            username = player_data["username"]
            pos_x = player_data["pos_x"]
            pos_y = player_data["pos_y"]

            for player in self.players:
                if player.username == username:
                    player.pos_x = pos_x
                    player.pos_y = pos_y
                    break
            else:
                self.players.append(User(username, pos_x, pos_y))

            self.send_udp("Player updated successfully", client_address)
        except Exception as e:
            print(f"Error updating player: {e}")
            self.send_udp("Error updating player", client_address)

    def send_all_players(self, client_address):
        """ Send all players' data. """
        try:
            players_data = {
                "num_players": len(self.players),
                "players": [{"username": p.username, "pos_x": p.pos_x, "pos_y": p.pos_y} for p in self.players]
            }

            self.send_udp(json.dumps(players_data), client_address)
        except Exception as e:
            print(f"Error sending players data: {e}")
            self.send_udp("Error sending players data", client_address)

    def handle_logout(self, client_address):
        """ Handle user logout. """
        try:
            data, _ = self.server_socket.recvfrom(1024)
            username = data.decode('utf-8')

            self.players = [p for p in self.players if p.username != username]
            self.send_udp("Logout successful", client_address)
        except Exception as e:
            print(f"Error during logout: {e}")
            self.send_udp("Error during logout", client_address)


if __name__ == "__main__":
    server = Server()
