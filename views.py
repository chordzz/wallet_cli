from repositories import *

class UserView:
    """Views relating to the user"""

    def __init__(self):
        self.user_repo = UserRepository()

    def signup(self, active_user):

        if active_user:
            print("You are logged in, logout to perform this action")
            return None
        else:
            name = input("Enter your full name, surname first: ")
            email = input("Enter your email address: ")
            phone = input("Enter your phone number: ")
            username = input('Enter your username: ')
            password = input("Enter your password: ")

            self.user_repo.create_user(name, email, phone, username, password)
            return None

    def signin(self, active_user):

        if active_user:
            print("You are logged in already, logout to perform this action")
            return active_user
        else:
            username = input("Enter your username: ")
            password = input("Enter your password: ")

            return self.user_repo.authenticate_user(username, password)

    def user(self, active_user):
        if not active_user:
            print("You need to be logged in to carry out this action")
            return
        self.user_repo.view_user()

    def signout(self, active_user):
        if not active_user:
            print("You need to be logged in to carry out this action")
            return
        self.user_repo.logout()

class WalletView:
    """Views relating to the wallet"""

    def __init__(self):
        self.wallet_repo = WalletRepository()

    def view_wallet(self, active_user):
        if not active_user:
            print("You need to be logged in to carry out this action")
            return
        self.wallet_repo.view_wallet(active_user['user_id'])

    def view_balance(self, active_user, ):
        if not active_user:
            print("You need to be logged in to carry out this action")
            return
        self.wallet_repo.view_balance(active_user['user_id'])

    def send(self, active_user):
        if not active_user:
            print("You need to be logged in to carry out this action")
            return
        receiver = input('Who would you like to transfer to? ')
        amount = input('How much do you want to send? ')
        self.wallet_repo.send(amount, active_user['username'], receiver, active_user['user_id'])

    def deposit(self, active_user):
        if not active_user:
            print("You need to be logged in to carry out this action")
            return
        
        amount = input("\nHow much would you like to deposit? ")
        self.wallet_repo.deposit(amount, active_user['user_id'], active_user['username'])

    def withdraw(self, active_user):
        if not active_user:
            print("You need to be logged in to carry out this action")
            return
        amount = input("\nHow much would you like to withdraw? ")
        self.wallet_repo.withdraw(amount, active_user['user_id'], active_user['username'])

class TransactionView:
    """Views relating to the transactions"""

    def __init__(self):
        self.transaction_repo = TransactionRepository()

    def view_transactions(self, active_user):
        if not active_user:
            print("You need to be logged in to carry out this action")
            return
        self.transaction_repo.view_transactions(active_user['username'])

    def view_single_transaction(self, active_user):
        transaction_id = input("Enter Transaction ID: ")
        self.transaction_repo.view_single_transaction(transaction_id)
    
