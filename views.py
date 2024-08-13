from repositories import *

from models import *

class UserView:
    """Views relating to the user"""

    def __init__(self):
        # self.user_repo = UserRepository()
        self.user_repo = UserRepositorySQL()

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
            user_id = random.random() * 999
            created_at = datetime.now().isoformat()

            new_user = User(name, email, phone, username, password, user_id, created_at)

            if self.user_repo.get_user_by_username(username):
                print("Username already exists")
                return

            if self.user_repo.create_new_user(new_user):
                wallet_id = random.random() * 777
                balance = 0
                created_at = datetime.now().isoformat()
                updated_at = datetime.now().isoformat()

                new_wallet = Wallet(wallet_id, balance, created_at, updated_at, user_id)
                try:
                    WalletRepositorySQL().create_wallet(new_wallet)
                    print("Wallet created.")
                except Exception as e:
                    print(f"Could not create wallet {e}")
                finally:
                    print("User Created.")
            else:
                print("Error creating user")

    def signin(self, active_user):

        if active_user:
            print("You are logged in already, logout to perform this action")
            return active_user
        else:
            username = input("Enter your username: ")
            password = input("Enter your password: ")

            if self.user_repo.signin_user(username, password):
                print("Login successful")
                return self.user_repo.get_user_by_username(username)
            print("Invalid credentials")
            return None
            
    def user(self, active_user):
        if not active_user:
            print("You need to be logged in to carry out this action")
            return
        print(self.user_repo.get_user_by_username(active_user.username).to_dict())

    def signout(self, active_user):
        if not active_user:
            print("You need to be logged in to carry out this action")
            return
        # self.user_repo.logout()
        print("Logged out")
        return None

class WalletView:
    """Views relating to the wallet"""

    def __init__(self):
        self.wallet_repo = WalletRepositorySQL()
        self.transaction_view = TransactionView()

    def view_wallet(self, active_user):
        if not active_user:
            print("You need to be logged in to carry out this action")
            return
        # self.wallet_repo.view_wallet(active_user['user_id'])
        wallet = self.wallet_repo.get_wallet_by_user_id(active_user.user_id)
        print(wallet.to_dict())

    def view_balance(self, active_user):
        if not active_user:
            print("You need to be logged in to carry out this action")
            return
        
        wallet = self.wallet_repo.get_wallet_by_user_id(active_user.user_id).wallet_id
        balance = self.wallet_repo.get_wallet_balance(wallet)
        print(balance)
        

    def send(self, active_user):
        if not active_user:
            print("You need to be logged in to carry out this action")
            return
        receiver = input('Who would you like to transfer to? ')
        amount = input('How much do you want to send? ')
        self.wallet_repo.send(amount, receiver, active_user)

    def deposit(self, active_user):
        if not active_user:
            print("You need to be logged in to carry out this action")
            return
        
        amount = float(input("\nHow much would you like to deposit? "))
        if not amount:
            print("Amount should be a valid number")
            return
        sender = self.wallet_repo.get_wallet_by_user_id(active_user.user_id).wallet_id
        
        self.transaction_view.create_transaction(amount, 'deposit', sender, '')
        

        # self.wallet_repo.deposit(amount, active_user)

    def withdraw(self, active_user):
        if not active_user:
            print("You need to be logged in to carry out this action")
            return
        amount = float(input("\nHow much would you like to withdraw? "))
        if not amount:
            print("Amount should be a valid number")
            return
        
        wallet = self.wallet_repo.get_wallet_by_user_id(active_user.user_id).wallet_id
        balance = self.wallet_repo.get_wallet_balance(wallet)

        if balance < amount:
            print("Insufficient Funds")
            return

        self.transaction_view.create_transaction(amount, 'withdrawal', wallet, '')
        # self.wallet_repo.withdraw(amount, active_user)

class TransactionView:
    """Views relating to the transactions"""

    def __init__(self):
        self.transaction_repo = TransactionRepositorySQL()
        self.wallet_repo = WalletRepositorySQL()
        self.user_repo = UserRepositorySQL()

    def create_transaction(self, amount, Ttype, sender, receiver):

        transaction_id = random.random() * 777
        created_at = datetime.now().isoformat()

        try:
            new_transaction = Transaction(transaction_id, amount, created_at, Ttype, sender, receiver)
            self.transaction_repo.create_transaction(new_transaction)
            print("Transaction successful")
            return True
        except Exception as e:
            print(f"Transaction failed \n {e}")
            return None

    def view_transactions(self, active_user):
        if not active_user:
            print("You need to be logged in to carry out this action")
            return
        wallet = self.wallet_repo.get_wallet_by_user_id(active_user.user_id).wallet_id

        all_transactions = self.transaction_repo.get_all_transactions(wallet)
        for t in all_transactions:
            print(t.to_dict())


    def view_single_transaction(self, active_user):
        if not active_user:
            print("You need to be logged in to carry out this action")
            return
        transaction_id = input("Enter Transaction ID: ")
        self.transaction_repo.view_single_transaction(transaction_id)

