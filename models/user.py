from flask_login import UserMixin


class User(UserMixin):
    def __init__(self, chats: list, id: int, email: str, password: str, name: str, surname: str, role: str,
                 created_at: str, blocked: bool, verified: bool, verification_code: int, address: str, rate: float,
                 profile_img_url: str, products: list, comments: list):
        self.chats = chats
        self.id = id
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
