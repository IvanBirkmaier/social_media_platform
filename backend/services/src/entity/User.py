class User:
    def __init__(self, id=None, username=None, email=None):
        self.id = id
        self.username = username
        self.email = email

    def get_username(self):
        return self.username

    def set_username(self, username):
        self.username = username

    def get_email(self):
        return self.email

    def set_email(self, email):
        self.email = email