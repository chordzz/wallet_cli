import random
from datetime import datetime

class User:
    """A class to represent a single user in the system"""

    def __init__(self, name, email, phone, username, password, user_id, created_at, wallet_id) -> None:
        """Initialize the user"""

        self.name = name
        self.email = email
        self.phone = phone
        self.username = username
        self.password = password
        self.user_id = user_id
        self.wallet_id = wallet_id
        self.created_at = created_at

    def set_wallet_id(self, wallet_id):
        self.wallet_id = wallet_id

    def to_dict(self):
        return {
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "username": self.username,
            "password": self.password,
            "user_id": self.user_id,
            "wallet_id": self.wallet_id,
            "created_at": self.created_at
        }

    def __repr__(self):
        return (f"User(user_id={self.user_id}, username={self.username}, email={self.email}, phone={self.phone}, name={self.name}, created_at={self.created_at}, status={self.status})")
        