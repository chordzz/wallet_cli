from repositories import *

@dataclass
class UserView:
    """Views relating to the user"""
    
    
    def __post_init__(self):
        self.user_repo = UserRepository()

    def signup(self):
        name = input("Enter your full name, surname first: ")
        email = input("Enter your email address: ")
        phone = input("Enter your phone number: ")
        username = input('Enter your username: ')
        password = input("Enter your password: ")

        self.user_repo.create_user(name, email, phone, username, password)

    def signin(self):

        username = input("Enter your username: ")
        password = input("Enter your password: ")

        return self.user_repo.authenticate_user(username, password)

    def user(self):
        self.user_repo.view_user()

    def signout(self):
        self.user_repo.logout()

@dataclass
class WalletView:
    """Views relating to the wallet"""

    def __post_init__(self):
        self.wallet_repo = WalletRepository()

    def view_wallet(self, user_id):
        self.wallet_repo.view_wallet(user_id)

    def view_balance(self, user_id):
        self.wallet_repo.view_balance(user_id)

    def send(self, user_id, sender):
        receiver = input('Who would you like to transfer to? ')
        amount = input('How much do you want to send? ')
        self.wallet_repo.send(amount, sender, receiver, user_id)


    def deposit(self, user_id, username):
        amount = input("\nHow much would you like to deposit? ")
        self.wallet_repo.deposit(amount, user_id, username)

    def withdraw(self, user_id, username):
        amount = input("\nHow much would you like to withdraw? ")
        self.wallet_repo.withdraw(amount, user_id, username)

@dataclass
class TransactionView:
    """Views relating to the transactions"""

    def __post_init__(self):
        self.transaction_repo = TransactionRepository()

    def view_transactions(self, username):
        self.transaction_repo.view_transactions(username)

    def view_single_transaction(self):
        transaction_id = input("Enter Transaction ID: ")
        self.transaction_repo.view_single_transaction(transaction_id)
    
