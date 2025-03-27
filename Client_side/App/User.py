class User:
    def __init__(self, username, pos_x, pos_y):
        self.username = username
        self.pos_x = pos_x
        self.pos_y = pos_y
    def print_all_users(self):
        print(self.username, self.pos_x, self.pos_y)