import sys
sys.path.append('C:\\Users\\Ivan\\Desktop\\social-media-platform\\backend\\')

from backend.entity.User import User


class UserDTO:
    def __init__(self, username, email):
        self.username = username
        self.email = email

    @staticmethod
    def from_entity(user):
        return UserDTO(username=user.username, email=user.email)

    def to_entity(self):
        return User(username=self.username, email=self.email)
