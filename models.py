from dataclasses import dataclass
from datetime import datetime


# @dataclass
class User:
    """Class for representing a user entity as a model"""

    def __init__(self, name='', email='', phone='', username='', password='', user_id='', created_at=''):
        self.name = name
        self.email = email
        self.phone = phone
        self.username = username
        self.password = password
        self.user_id = user_id
        self.created_at = created_at


    def to_dict(self):
        return {
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "username": self.username,
            "password": self.password,
            "user_id": self.user_id,
            # "wallet_id": self.wallet_id,
            "created_at": self.created_at
        }
    
@dataclass
class Wallet:
    """A class to represent a single wallet in the system"""

    def __init__(self, wallet_id='', balance=0, created_at='', updated_at='', user_id=''):
        self.wallet_id = wallet_id
        self.balance = balance
        self.user_id = user_id
        self.created_at = created_at
        self.updated_at = updated_at
    
    # wallet_id: str
    # balance: float
    # user_id: str
    # created_at: str
    # updated_at: str


    def deposit(self, amount):
        print(self.wallet_id)
        self.balance += float(amount)
        self.updated_at = datetime.now().isoformat()
        print('deposit')
        return True

    def withdraw(self, amount):
        amount = float(amount)
        print(self.wallet_id)
        if self.balance >= amount:
            self.balance -= amount
            self.updated_at = datetime.now().isoformat()
            print('withdraw')
            return True
        else:
            print('not done')
            return False

    def to_dict(self):
        return {
            "wallet_id": self.wallet_id,
            "balance": self.balance,
            "user_id": self.user_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
@dataclass
class Transaction:
    """A class to represent a single transaction in the system"""

    def __init__(self, transaction_id='', amount=0.0, created_at='', Ttype='', sender='', receiver=''):
        self.transaction_id = transaction_id
        self.created_at = created_at
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.Ttype = Ttype

    def to_dict(self):
        return {
            "transaction_id": self.transaction_id,
            "created_at": self.created_at,
            "sender": self.sender,
            "receiver": self.receiver,
            "amount": self.amount,
            "Ttype": self.Ttype
        }

