from flask_login import UserMixin
from datetime import datetime


class User(UserMixin):
    def __init__(self, _id: str, email: str, password: str, name: str, surname: str, role: str,
                 address: str, created_at: str = str(datetime.now()), rate: float = 0, products: list = None,
                 comments: list = None, chats: list = None, blocked: bool = False, verified: bool = False,
                 verification_code: int = -1, profile_img_url: str = "deneme.url"):
        self._id = _id
        self.chats = chats
        self.email = email
        self.password = password
        self.name = name
        self.surname = surname
        self.role = role
        self.created_at = created_at
        self.blocked = blocked
        self.verified = verified
        self.verification_code = verification_code
        self.address = address
        self.rate = rate
        self.profile_img_url = profile_img_url
        self.products = products
        self.comments = comments
        self.active = True

    def get_id(self):
        return self.email

    @property
    def is_active(self):
        return self.active
