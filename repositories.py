import random
from dataclasses import dataclass, field
from datetime import datetime

from helpers import *
from models import *

user_db_path = "data/users.json"
wallet_db_path = "data/wallets.json"
transactions_db_path = "data/transactions.json"

@dataclass
class UserRepository:
    """Data interactions for the User model"""

    users: list = field(default_factory=list)
    # user: User = field(default_factory=User)

    def __post_init__(self):
        self.users = read_from_db(user_db_path)
        if not self.users:
            self.users = []

    def create_user(self, name, email, phone, username, password):

        if self.users:
            for user in self.users:
                if user['username'] == username:
                    print('User already exists, try signing up with different details')
                    return
        
        user_id = random.random() * 999
        created_at = datetime.now().isoformat()

        try:
            wallet_repo = WalletRepository()
            wallet_repo.create_wallet(user_id)
        except:
            print("Something went wrong while creating your wallet, please try signing up again")
            return
        else:
            new_user = {
                "name": name,
                "email": email,
                "phone": phone,
                "username": username,
                "password": password,
                "user_id": user_id,
                "created_at": created_at
            }
            self.users.append(new_user)
            
            write_to_db(user_db_path, self.users)
            print("User created")

    def authenticate_user(self, username, password):
        """Authentication function for users"""

        for user in self.users:
            if user['username'] == username and user['password'] == password:
                print("Logged in")
                self.user = user
                return user
            
        print("\nIncorrect sign-in details, please try again\n")
        return None
    
    def view_user(self):
        print(f"My Profile: {json.dumps(self.user, indent=4)}")
        
    def logout(self):
        self.user = {}
        print('logged out')
        return {}
    
@dataclass
class WalletRepository:
    """Data interactions for the Wallet model"""

    wallets: list = field(default_factory=list)
    wallet: Wallet = field(default_factory=Wallet)

    def __post_init__(self):
        self.wallets = read_from_db(wallet_db_path)
        if not self.wallets:
            self.wallets = []

    def create_wallet(self, user_id):
        wallet_id = random.random() * 777
        balance = 0
        created_at = datetime.now().isoformat()
        updated_at = datetime.now().isoformat()
        user_id = user_id

        new_wallet = {
            "wallet_id": wallet_id,
            "balance": balance,
            "user_id": user_id,
            "created_at": created_at,
            "updated_at": updated_at
        }
        self.wallets.append(new_wallet)

        try:
            write_to_db(wallet_db_path, self.wallets)
        except:
            print("Error creating wallet")
        else:
            print("Wallet created")

    def view_wallet(self, user_id):
        self.set_active_wallet(user_id)
        print(f"My Wallet: {json.dumps(self.wallet.to_dict(), indent=4)}")
    
    def set_active_wallet(self, user_id):
        
        for wallet in self.wallets:
            if wallet['user_id'] == user_id:
                self.wallet = Wallet(wallet['wallet_id'], wallet['balance'], wallet['user_id'], wallet['created_at'], wallet['updated_at'])
    
    def deposit(self, amount, user_id, username):

        self.set_active_wallet(user_id)

        try:
            if self.wallet.deposit(amount):
                for wallet in self.wallets:
                    if wallet['wallet_id'] == self.wallet.wallet_id:
                        wallet['balance'] = self.wallet.balance

                        transaction_repo = TransactionRepository()
                        transaction_repo.create_transaction(username,  amount, 'deposit', receiver='')
                        write_to_db(wallet_db_path, self.wallets)
            
            print(f"You have deposited #{amount}. Balance = {self.wallet.balance}")
            self.wallets = read_from_db(wallet_db_path)

        except ValueError:
            print('Amount can only contain numbers')
    
    def withdraw(self, amount, user_id, username):

        self.set_active_wallet(user_id)

        try:
            if self.wallet.withdraw(amount):
                for wallet in self.wallets:
                    if wallet['wallet_id'] == self.wallet.wallet_id:
                        wallet['balance'] = self.wallet.balance

                        transaction_repo = TransactionRepository()
                        transaction_repo.create_transaction(username, amount, 'withdrawal', receiver='')
                        write_to_db(wallet_db_path, self.wallets)
            
            print(f"You have withdrawn #{amount}. Balance = {self.wallet.balance}")
            self.wallets = read_from_db(wallet_db_path)

        except ValueError:
            print('Amount can only contain numbers')

    def send(self, amount, sender, receiver, user_id):
        """Function to send money to another user"""
        
        user_repo = UserRepository()
        self.set_active_wallet(user_id)
        print(self.wallet.balance)
        print(float(amount))
        
        try:
            if self.wallet.balance >= float(amount):
                for user in user_repo.users:
                    if user['username'] == receiver:
                        for wallet in self.wallets:
                            if wallet['user_id'] == user['user_id']:
                                self.set_active_wallet(wallet['user_id'])
                                self.wallet.deposit(amount)

                                for mywallet in self.wallets:
                                    if mywallet['wallet_id'] == self.wallet.wallet_id:
                                        mywallet['balance'] = self.wallet.balance

                                self.set_active_wallet(user_id)
                                self.wallet.withdraw(amount)

                                for mywallet in self.wallets:
                                    if mywallet['wallet_id'] == self.wallet.wallet_id:
                                        mywallet['balance'] = self.wallet.balance

                                transaction_repo = TransactionRepository()
                                transaction_repo.create_transaction(sender, amount, 'debit-transfer', receiver)
                                transaction_repo.create_transaction(sender, amount, 'credit-transfer', receiver)

                                write_to_db(wallet_db_path, self.wallets)

                                return
                                
                print("It seems the user you are trying to send money to does not exist.")
                return
            print('Insufficient Funds')
            return
        except ValueError:
            print('Amount can only contain numbers')
    
    def view_balance(self, user_id):
        self.set_active_wallet(user_id)
        print("\nYour account balance is: ", self.wallet.balance)
    
@dataclass
class TransactionRepository:
    """Data interactions for the Transaction model"""

    transactions: list = field(default_factory=list)

    def __post_init__(self):
        self.transactions = read_from_db(transactions_db_path)
        if not self.transactions:
            self.transactions = []

    def create_transaction(self, sender, amount, Ttype, receiver):
        """Function to create a transaction"""
        transaction_id = random.random() * 999999
        created_at = datetime.now().isoformat()
        
        new_transaction = {
            "sender": sender,
            "receiver": receiver,
            "amount": amount,
            "Ttype": Ttype,
            "transaction_id": transaction_id,
            "created_at": created_at
        }

        self.transactions.append(new_transaction)
        write_to_db(transactions_db_path, self.transactions)
        self.transactions = read_from_db(transactions_db_path)

    def view_transactions(self, username):

        transactions = [t for t in self.transactions if (t['sender'] == username and not (t['Ttype'] == 'credit-transfer')) or (t['receiver'] == username and t['Ttype'] == 'credit-transfer')]

        if not transactions:
            print("\nYou have no transactions yet")
            return
        print(f"\nTransactions: {json.dumps(transactions, indent=4)}")
    
    def view_single_transaction(self, transaction_id):
        for t in self.transactions:
            if t['transaction_id'] == float(transaction_id):
                print(f"Transaction: {json.dumps(t, indent=4)}")
                return
        print("Transaction not found")