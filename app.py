from user import User
from wallet import Wallet
from transaction import Transaction

import random
from datetime import datetime
import json
from time import sleep


class App:
    """Main App flow"""

    def __init__(self) -> None:

        self.app_active = None
        self.users = []
        self.wallets = []
        self.transactions = []

        self.user = None
        self.wallet = None

        self.user_db_path = "data/users.json"
        self.wallet_db_path = "data/wallets.json"
        self.transactions_db_path = "data/transactions.json"

    def run_app(self):
        """Start main app"""

        self.app_active = True

        print("Welcome to your HB wallet...")
        print("please wait while we setup your app")
        sleep(2)

        self._read_from_users_db()
        self._read_from_wallets_db()
        self._read_from_transactions_db()
        print("App Setup Complete")

        # Start main app flow
        while self.app_active:
            sleep(1)
            self.user = {}
            self.wallet = {}

            print("\nEnter the corresponding numbers to perform an action.")
            user_input = input("1. Create Account\n"
                               "2. Sign-in to your Account\n"
                               "3. Exit App \n"
                               )
            if user_input == '1':
                self._sign_up_flow()

            elif user_input == '2':
                username = input("Enter your username: ")
                password = input("Enter your password: ")

                active_user = self._authenticate_user(username, password)

                if active_user:
                    print("Logged in")
                    sleep(1)
                    self.user = active_user[0]
                    self.wallet = active_user[1]
                    self._sign_in_flow()

            else:
                print("\nByeeeeeee!!!")
                return

    def _authenticate_user(self, input_username, input_password):
        """Authentication function for users"""
        for user in self.users:
            if user.username == input_username and user.password == input_password:
                for wallet in self.wallets:
                    if user.wallet_id == wallet.wallet_id:
                        return [user, wallet]
                print("\nSomething went wrong with your wallet, consider creating a new account\n")
                return None
        print("\nIncorrect sign-in details, please try again\n")
        return None

    def _create_user(self):
        name = input("Enter your full name, surname first: ")
        email = input("Enter your email address: ")
        phone = input("Enter your phone number: ")

        # check if username already existed in json file
        username = input("Enter your username: ")
        try:
            with open(self.user_db_path, 'r') as file:
                if any(user_['username'] == username for user_ in json.load(file)):
                    print('Username already existed')
                    return
        except json.JSONDecodeError:
            pass

        password = input("Enter your password: ")
        user_id = random.random() * 999
        created_at = datetime.now().isoformat()
        wallet_id = None

        return User(name, email, phone, username, password, user_id, created_at, wallet_id)

    def _create_wallet(self, user):
        wallet_id = random.random() * 777
        balance = 0
        created_at = datetime.now().isoformat()
        updated_at = datetime.now().isoformat()
        return Wallet(user, wallet_id, balance, created_at, updated_at)

    def _create_transaction(self, sender, amount, Ttype, receiver=""):
        """Function to create a transaction"""
        transaction_id = random.random() * 999999
        created_at = datetime.now().isoformat()
        transaction = Transaction(sender, amount, Ttype, transaction_id, created_at, receiver)
        self.transactions.append(transaction)
        return transaction

    def _sign_up_flow(self):
        """ The signup process flow of the app"""

        try:
            self.user = self._create_user()
        except ValueError:
            print("Error creating user, please try again")
            return
        else:
            try:
                self.wallet = self._create_wallet(self.user.user_id)
            except ValueError:
                print("Error creating wallet, please try again")
            else:
                self.user.set_wallet_id(self.wallet.wallet_id)
                self.wallets.append(self.wallet)
                self.users.append(self.user)

                self._write_to_db(self.user_db_path, [user.to_dict() for user in self.users])
                self._write_to_db(self.wallet_db_path, [wallet.to_dict() for wallet in self.wallets])

                print("User created successfully")
                print("Wallet created successfully")
                print("Signup Successful")

    def _sign_in_flow(self):
        """Function with the flow for signing in"""

        logged_in = True
        sleep(1)
        while logged_in:
            print("\n")
            user_input = input("1. Deposit Money \n"
                               "2. Withdraw Money \n"
                               "3. Send Money \n"
                               "4. Check Balance \n"
                               "5. My Transactions \n"
                               "6. My wallet\n"
                               "7. My Profile\n"
                               "8. View single transaction\n"
                               "9. Sign out \n"
                               )
            if user_input == '1':
                self._deposit()
            elif user_input == '2':
                amount = input("Enter the amount you want to withdraw: ")
                self._withdraw(amount)
            elif user_input == '3':
                receiver = input("Enter the username of the receiver: ")
                # catch non integer values
                try:
                    amount = input("Enter the amount to you want to send: ")
                    self._send_money(amount, receiver)
                except ValueError:
                    print('Ensure all values are in numbers')
            elif user_input == '4':
                self._view_balance()
            elif user_input == '5':
                self._view_transactions()
            elif user_input == '6':
                self._view_wallet()
            elif user_input == '7':
                self._view_profile()
            elif user_input == '8':
                # catch errors for invalid ID number
                try:
                    id = input("Enter transaction ID: ")
                    self._view_single_transaction(float(id))
                except ValueError:
                    print('Incorrect transaction number')
                    continue

            elif user_input == '9':
                print("User Logged out")
                logged_in = False
            else:
                print("\ninvalid input\n")
                sleep(0.5)

    def _write_to_db(self, path, data):
        """Function to write to any DB"""
        w = open(path, 'w')
        w.write(json.dumps(data, indent=4))
        w.close()

    def _read_from_users_db(self):
        """Function to read from users db"""
        sleep(1)
        # Load in the users DB, create it if it doesn't exist
        try:
            users_fr = open("data/users.json", 'r')
            user_dicts = json.load(users_fr)
            self.users = [User(**user_dict) for user_dict in user_dicts]
            print("User DB loaded successfully")
        except FileNotFoundError:
            print("User DB not found, creating one now")
            open("data/users.json", 'x').close()
        except json.decoder.JSONDecodeError:
            print("User DB is empty or corrupted, reinitializing")
            print("Reinitialization complete")
            self.users = []

    def _read_from_wallets_db(self):
        """ Function to read from wallets db """
        sleep(1)
        # Load in the wallets DB, create it if it doesn't exist
        try:
            wallets_fr = open("data/wallets.json", 'r')
            wallet_dicts = json.load(wallets_fr)
            self.wallets = [Wallet(**wallet_dict) for wallet_dict in wallet_dicts]
            print("Wallet DB loaded successfully")
        except FileNotFoundError:
            print("Wallets DB not found, creating one now")
            open("data/wallets.json", 'x').close()
        except json.decoder.JSONDecodeError:
            print("Wallets DB is empty or corrupted, reinitializing")
            print("Reinitialization complete")

    def _read_from_transactions_db(self):
        """ Function to read from wallets db """
        sleep(1)
        # Load in the Transactions DB, create it if it doesn't exist
        try:
            transaction_fr = open("data/transactions.json", 'r')
            transaction_dicts = json.load(transaction_fr)
            self.transactions = [Transaction(**transaction_dict) for transaction_dict in transaction_dicts]
            print("Transactions DB loaded successfully")
        except FileNotFoundError:
            print("Transactions DB not found, creating one now")
            open("data/transactions.json", 'x').close()
        except json.decoder.JSONDecodeError:
            print("Transactions DB is empty or corrupted, reinitializing")
            print("Reinitialization complete")

    def _deposit(self):
        sleep(1)
        amount = input("\nHow much would you like to deposit? ")
        if self.wallet.deposit(amount):
            for wallet in self.wallets:
                if wallet.wallet_id == self.wallet.wallet_id:
                    wallet.balance = self.wallet.balance
                    break

        self._create_transaction(self.user.username, amount, "deposit")

        self._write_to_db(self.transactions_db_path, [t.to_dict() for t in self.transactions])
        self._write_to_db(self.wallet_db_path, [wallet.to_dict() for wallet in self.wallets])
        self._read_from_transactions_db()
        self._read_from_wallets_db()
        print(f"You have deposited #{amount}. Balance = {self.wallet.balance}")

    def _withdraw(self, amount):
        """Function to withdraw money"""
        sleep(0.5)
        amount = float(amount)

        if self.wallet.withdraw(amount):
            for wallet in self.wallets:
                if wallet.wallet_id == self.wallet.wallet_id:
                    wallet.balance = self.wallet.balance
                    break
            self._create_transaction(self.user.username, amount, "withdrawal")
            self._write_to_db(self.wallet_db_path, [wallet.to_dict() for wallet in self.wallets])
            self._write_to_db(self.transactions_db_path, [t.to_dict() for t in self.transactions])
            self._read_from_transactions_db()
            self._read_from_wallets_db()
            print(f"Your new balance is: {self.wallet.balance}")
        else:
            print("Insufficient Funds")

    def _send_money(self, amount, receiver):
        """Function to send money to another user"""

        amount = float(amount)

        if not amount:
            print("invalid amount")
            return

        # stop being able to send money to self, if sender is same as receiver
        if self.user.username == receiver:
            print("Sorry you cannot send money to yourself.")
            return
        else:
            if self.wallet.balance >= amount:
                for user in self.users:
                    if user.username == receiver:
                        for wallet in self.wallets:
                            if wallet.user_id == user.user_id:
                                wallet.deposit(amount)
                                self.wallet.withdraw(amount)
                                print(self.wallet)
                                print(self.wallets)

                                self._create_transaction(self.user.username, amount, "debit-transfer", user.username)
                                self._create_transaction(self.user.username, amount, "credit-transfer", user.username)

                                self._write_to_db(self.transactions_db_path, [t.to_dict() for t in self.transactions])

                                self._write_to_db(self.wallet_db_path, [w.to_dict() for w in self.wallets])

                                self._read_from_wallets_db()
                                self._read_from_transactions_db()
                                print(f"Money sent to {receiver}")
                                return
                print("It seems the user you're trying to send to does not exist")
            else:
                print("Insufficient Funds")

    def _view_balance(self):
        sleep(0.5)
        print("\nYour account balance is: ", self.wallet.balance)

    def _view_transactions(self):
        """Functions to show all transactions"""

        all_transactions = [t.to_dict() for t in self.transactions if t.sender == self.user.username or (
                    t.receiver == self.user.username and t.Ttype == 'credit-transfer')]

        if not all_transactions:
            print("\nYou have no transactions yet")
            return
        sleep(1)
        print(f"\nAll Transactions: {json.dumps(all_transactions, indent=4)}")

    def _view_profile(self):
        sleep(0.5)
        print(f"My Profile: {json.dumps(self.user.to_dict(), indent=4)}")

    def _view_wallet(self):
        sleep(0.5)
        print(f"My Wallet: {json.dumps(self.wallet.to_dict(), indent=4)}")

    def _view_single_transaction(self, id):
        for t in self.transactions:
            if t.transaction_id == id:
                print(f"Transaction: {json.dumps(t.to_dict(), indent=4)}")
                return
        print("Transaction not found")


if __name__ == '__main__':
    app = App()
    app.run_app()