import random
from datetime import datetime


class Wallet:
    """A class to represent a single wallet in the system"""

    def __init__(self, user_id, wallet_id, balance, created_at, updated_at) -> None:
        """Initialize the wallet"""

        self.wallet_id = wallet_id
        self.balance = balance
        self.user_id = user_id
        self.created_at = created_at
        self.updated_at = updated_at

    def to_dict(self):
        return {
            "wallet_id": self.wallet_id,
            "balance": self.balance,
            "user_id": self.user_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    def deposit(self, amount):
        self.balance += float(amount)
        self.updated_at = datetime.now().isoformat()

    def withdraw(self, amount):
        if self.balance >= amount:
            self.balance -= amount
            self.updated_at = datetime.now().isoformat()
            return True
        else:
            return False

    def __repr__(self):
        return f"Wallet(wallet_id={self.wallet_id}, balance={self.balance}, user_id={self.user_id}, created_at={self.created_at}, updated_at={self.updated_at})"