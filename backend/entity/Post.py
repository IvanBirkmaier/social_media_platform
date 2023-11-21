class Post:
    def __init__(self, id=None, image=None, text=None, user_id=None, timestamp=None):
        self.id = id
        self.image = image
        self.text = text
        self.user_id = user_id
        self.timestamp = timestamp

    def get_image(self):
        return self.image

    def set_image(self, image):
        self.image = image

    def get_text(self):
        return self.text

    def set_text(self, text):
        self.text = text

    def get_user(self):
        return self.user

    def set_user(self, user):
        self.user = user