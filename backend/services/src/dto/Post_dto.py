import sys
sys.path.append('C:\\Users\\Ivan\\Desktop\\social-media-platform\\backend\\')

from backend.services.src.dto.User_dto import UserDTO
from backend.entity.Post import Post


class PostDTO:
    def __init__(self, image, text, user_dto):
        self.image = image
        self.text = text
        self.user_dto = user_dto

    @staticmethod
    def from_entity(post):
        user_dto = UserDTO.from_entity(post.user) if post.user else None
        return PostDTO(image=post.image, text=post.text, user_dto=user_dto)

    def to_entity(self):
        user = self.user_dto.to_entity() if self.user_dto else None
        return Post(image=self.image, text=self.text, user=user)

# A data transfer object (DTO) is an object that carries data between processes.
# You can use this technique to facilitate communication between two systems (like an API and your server)
# without potentially exposing sensitive information.