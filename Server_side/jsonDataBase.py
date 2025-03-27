import json

class jsonDataBase:
    def __init__(self, filename="data.json"):
        self.filename = filename
        try:
            # Try to load existing JSON data from the file
            with open(self.filename, 'r') as file:
                self.data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            # If the file doesn't exist or is empty, initialize with an empty list
            self.data = []

    def add_entry(self, title, content, username, pos_x, pos_y):
        """
        Adds an entry with a title, content, username, pos_x, and pos_y to the JSON data.
        """
        entry = {
            "title": title.strip(),
            "content": content.strip(),
            "username": username.strip(),
            "pos_x": pos_x,
            "pos_y": pos_y
        }
        self.data.append(entry)
        self.save()

    def get_data(self):
        """
        Returns all the entries in the JSON data.
        """
        return self.data

    def receive_data(self):
        """
        Returns four lists: one for titles, one for contents, one for usernames, and one for positions.
        """
        titles = [entry['title'] for entry in self.data]
        contents = [entry['content'] for entry in self.data]
        usernames = [entry['username'] for entry in self.data]
        pos_x = [entry['pos_x'] for entry in self.data]
        pos_y = [entry['pos_y'] for entry in self.data]
        return titles, contents, usernames, pos_x, pos_y

    def save(self):
        """
        Saves the JSON data to the file.
        """
        with open(self.filename, 'w') as file:
            json.dump(self.data, file, indent=4)
