from user import User
from wallet import Wallet
from transaction import Transaction

import random
from datetime import datetime
from pathlib import Path
import json
from time import sleep

class App:
    """Main App flow"""

    def __init__(self) -> None:
        # fr = open("data/users.json", 'r')
        # self.users = json.load(fr)

        self.users = []
        self.wallets = []
        self.transactions = []

        self.user = {}
        self.wallet = {}

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
            if user["username"] == input_username and user["password"] == input_password:
                for wallet in self.wallets:
                    if user["wallet_id"] == wallet["wallet_id"]:
                        return [user, wallet]
                print("\nSomething went wrong with your wallet, consider creating a new account\n")
                return None
        print("\nIncorrect sign-in details, please try again\n")
        return None

    def _create_user(self):
        new_user = {}
        new_user["name"] = input("Enter your full name, surname first: ")
        new_user["email"] = input("Enter your email address: ")
        new_user["phone"] = input("Enter your phone number: ")
        new_user["username"] = input("Enter your username: ")
        new_user["password"] = input("Enter your password: ")
        new_user["user_id"] = random.random() * 999
        new_user["created_at"] = datetime.now().isoformat()
        self.user = new_user

    def _create_wallet(self):
        new_wallet = {}
        new_wallet["wallet_id"] = random.random() * 777
        new_wallet["balance"] = 0
        new_wallet["user_id"] = self.user["user_id"]
        new_wallet["created_at"] = datetime.now().isoformat()
        new_wallet["updated_at"] = datetime.now().isoformat()
        # self.wallet = Wallet(new_wallet)
        self.wallet = new_wallet

    def _create_transaction(self, sender, amount, Ttype, receiver=""):
        """Function to create a transaction"""
        new_transaction = {}
        new_transaction["transaction_id"] = random.random() * 999999
        new_transaction["created_at"] = datetime.now().isoformat()
        new_transaction["sender"] = sender
        new_transaction["receiver"] = receiver
        new_transaction["amount"] = int(amount)
        new_transaction["type"] = Ttype

        self.transactions.append(new_transaction)

    def _sign_up_flow(self):
        """ The signup process flow of the app"""

        try:
            self._create_user()
        except:
            print("Error creating user, please try again")
            # self.app_active = False
        else:
            try:
                self._create_wallet()
            except:
                print("Error creating wallet, please try again")
            else:
                self.user["wallet_id"] = self.wallet["wallet_id"]
                self.wallets.append(self.wallet)
                self.users.append(self.user)

                self._write_to_db(self.user_db_path, self.users)
                self._write_to_db(self.wallet_db_path, self.wallets)

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
                amount = input("Enter the amount to you want to send: ")
                self._send_money(amount, receiver)
            elif user_input == '4':
                self._view_balance()
            elif user_input == '5':
                self._view_transactions()
            elif user_input == '6':
                self._view_wallet()
            elif user_input == '7':
                self._view_profile()
            elif user_input == '8':
                id = input("Enter transaction ID: ")
                self._view_single_transaction(float(id))
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
            self.users = json.load(users_fr)
            print("User DB loaded successfully")
        except FileNotFoundError:
            print("User DB not found, creating one now")
            open("data/users.json", 'x')
        except json.decoder.JSONDecodeError:
            print("User DB is empty or corrupted, reinitializing")
            print("Reinitialization complete")

    def _read_from_wallets_db(self):
        """ Function to read from wallets db """
        sleep(1)
        # Load in the wallets DB, create it if it doesn't exist
        try:
            wallets_fr = open("data/wallets.json", 'r')
            self.wallets = json.load(wallets_fr)
            print("Wallet DB loaded successfully")
        except FileNotFoundError:
            print("Wallets DB not found, creating one now")
            open("data/wallets.json", 'x')
        except json.decoder.JSONDecodeError:
            print("Wallets DB is empty or corrupted, reinitializing")
            print("Reinitialization complete")

    def _read_from_transactions_db(self):
        """ Function to read from wallets db """
        sleep(1)
        # Load in the Transactions DB, create it if it doesn't exist
        try:
            transaction_fr = open("data/transactions.json", 'r')
            self.transactions = json.load(transaction_fr)
            print("Transactions DB loaded successfully")
        except FileNotFoundError:
            print("Transactionss DB not found, creating one now")
            open("data/transactionss.json", 'x')
        except json.decoder.JSONDecodeError:
            print("Transactionss DB is empty or corrupted, reinitializing")
            print("Reinitialization complete")

    def _deposit(self):
        sleep(1)
        amount = input("\nHow much would you like to deposit? ")
        for wallet in self.wallets:
            if self.wallet["wallet_id"] == wallet["wallet_id"]:
                wallet["balance"] += int(amount)
                sleep(1)
                print(f"You have deposited #{amount}. Balance = {wallet['balance']}")
                self.wallet = wallet
                self._create_transaction(self.user["username"], amount, "deposit" )

                self._write_to_db(self.transactions_db_path, self.transactions)
                self._write_to_db(self.wallet_db_path, self.wallets)
                self._read_from_transactions_db()
                self._read_from_wallets_db()

    def _withdraw(self, amount):
        """Function to withdraw money"""
        sleep(0.5)
        for wallet in self.wallets:
            if self.wallet["wallet_id"] == wallet["wallet_id"]:
                if wallet["balance"] >= int(amount):
                    wallet["balance"] -= int(amount)
                    sleep(1)
                    print(f"Your new balance is: {wallet['balance']}")
                    self.wallet = wallet
                    self._create_transaction(self.user["username"], amount, "withdrawal" )

                    self._write_to_db(self.wallet_db_path, self.wallets)
                    self._write_to_db(self.transactions_db_path, self.transactions)
                    self._read_from_transactions_db()
                    self._read_from_wallets_db()
                    return
                else:
                    print("Insufficient Funds")
                    return
        print("Something went wrong with your wallet")

    def _send_money(self, amount, receiver):
        """Function to send money to another user"""

        # Check if user has enough to send
        for user in self.users:
            if user["username"] == self.user["username"]:
                for wallet in self.wallets:
                    if wallet["wallet_id"] == user["wallet_id"]:
                        if wallet["balance"] >= int(amount):

                            # Actual sending
                            for user2 in self.users:
                                if user2["username"] == receiver:
                                    for wallet2 in self.wallets:
                                        if wallet2["wallet_id"] == user2["wallet_id"]:
                                            wallet2["balance"] += int(amount)
                                            wallet["balance"] -= int(amount)
                                            print(f"Money sent to {receiver}")
                                            sleep(1)
                                            self.wallet = wallet

                                            self._create_transaction(self.user["username"], amount, "debit-transfer", user2["username"])
                                            self._create_transaction(self.user["username"], amount, "credit-transfer", user2["username"])

                                            self._write_to_db(self.transactions_db_path, self.transactions)

                                            self._write_to_db(self.wallet_db_path, self.wallets)
                                            self._read_from_wallets_db()
                                            self._read_from_transactions_db()
                                            return
                                        
                            print("it seems the user you're trying to send to does not exist")
                            return
                        else:
                            print("Insufficient Funds")
                            return

    def _view_balance(self):
        sleep(0.5)
        print("\nYour account balance is: ", self.wallet["balance"])

    def _view_transactions(self):
        """Functions to show all transactions"""

        all_transactions = []

        for t in self.transactions:
            if t["sender"] == self.user["username"]:
                all_transactions.append(t)
            if t["receiver"] == self.user["username"] and t["type"] == 'credit-transfer':
                all_transactions.append(t)
        
        if not all_transactions:
            print("\nYou have no transactions yet")
            return
        sleep(1)
        print(f"\nAll Transactions: {all_transactions}")

    def _view_profile(self):
        sleep(0.5)
        print(f"My Profile: {self.user}")

    def _view_wallet(self):
        sleep(0.5)
        print(f"My Wallet: {self.wallet}")   
        
    def _view_single_transaction(self, id):
        for t in self.transactions:
            if t["transaction_id"] == id:
                print(f"Transaction: {t}")
                return 
        print("Transaction not found")        


if __name__ == '__main__':
    app = App()
    app.run_app()
