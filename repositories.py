import random
from dataclasses import dataclass, field
from datetime import datetime

from helpers import *
from models import *
from controller import setup_postgres

user_db_path = "data/users.json"
wallet_db_path = "data/wallets.json"
transactions_db_path = "data/transactions.json"

setup_postgres()

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

######################################## SQL ################################

class UserRepositorySQL:

    @staticmethod
    def create_user(name, email, phone, username, password):
        conn = connect_to_db()
        check_user_exist_query = """
            SELECT username FROM users WHERE username = %s
        """

        new_user_query = """
            INSERT INTO users (name, email, phone, username, password, user_id, created_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s);
        """

        if conn:
            with conn.cursor() as cur:
                cur.execute(check_user_exist_query, (username,))
                if cur.fetchone():
                    print('User already exists, try signing up with different details')
                    return
            
            user_id = random.random() * 999
            created_at = datetime.now().isoformat()

            wallet_repo = WalletRepositorySQL()

            try:
                with conn.cursor() as cur:
                    cur.execute(new_user_query, (name, email, phone, username, password, user_id, created_at))
                    conn.commit()
                    print("User created")
                    wallet_repo.create_wallet(user_id)

            except Exception as e:
                print(f"Something went wrong while creating your user: {e}")
                conn.rollback()
            finally:
                conn.close()

    @staticmethod
    def authenticate_user(username, password):
        conn = connect_to_db()
        get_user_query = """
            SELECT name, email, phone, username, user_id, created_at
            FROM users WHERE username = %s and password = %s
        """

        if conn:
            with conn.cursor() as cur:
                cur.execute(get_user_query, (username, password))
                user = cur.fetchone()
                print(user)
                if user:
                    user = User(*user)
                    print("Logged in successfully")
                    return(user)
                else:
                    print('Invalid login credentials')

    @staticmethod
    def view_user(username):
        conn = connect_to_db()

        if conn:
            try:
                with conn.cursor() as cur:
                    cur.execute("SELECT * FROM users WHERE username = %s", (username,))
                    user = cur.fetchone()
                    
                    if user is None:
                        print("user not found")
                        return user
                    print(user)
            except Exception as e:
                print(f"Something went wrong: {e}")
                conn.rollback()
            finally:
                conn.close()

class WalletRepositorySQL:

    @staticmethod
    def create_wallet(user_id):
        conn = connect_to_db()

        new_wallet_query = """
            INSERT INTO wallets (wallet_id, balance, created_at, updated_at, user_id)
            VALUES (%s, %s, %s, %s, %s);
        """

        if conn:
            try:
                with conn.cursor() as cur:
                    wallet_id = random.random() * 777
                    balance = 0
                    created_at = datetime.now().isoformat()
                    updated_at = datetime.now().isoformat()

                    cur.execute(new_wallet_query, (wallet_id, balance, created_at, updated_at, user_id))
                    conn.commit()
                    print("Wallet created")
            except Exception as e:
                print(f"Something went wrong while creating your wallet: {e}")
                conn.rollback()
                return
            finally:
                conn.close()

    @staticmethod
    def send(amount, receiver, sender):
        conn = connect_to_db()
        transaction_repo = TransactionRepositorySQL()

        update_wallet_query = """
            UPDATE wallets SET balance = %s WHERE user_id = %s;
        """

        get_receiver_query = """
            SELECT name, email, phone, username, user_id, created_at
            FROM users WHERE username = %s"""
        
        if receiver == sender.username:
            print("You cannot send money to yourself")
            return

        if conn:
            try:
                amount = float(amount)  # Convert the amount to float
                with conn.cursor() as cur:
                    # Get receiver data
                    cur.execute(get_receiver_query, (receiver,))
                    receiver_data = cur.fetchone()
                    if receiver_data is None:
                        print("The user you are trying to send to does not exist")
                        return
                    if receiver_data:
                        print(receiver_data)
                        receiver_data = User(*receiver_data)

                    # Get the sender's current balance
                    cur.execute("SELECT balance FROM wallets WHERE user_id = %s", (sender.user_id,))
                    sender_balance = cur.fetchone()
                    if sender_balance is None:
                        print("Sender not found")
                        return
                    sender_balance = sender_balance[0]

                    # Get the receiver's current balance
                    cur.execute("SELECT balance FROM wallets WHERE user_id = %s", (receiver_data.user_id,))
                    receiver_balance = cur.fetchone()
                    print(f"receiver balance: {receiver_balance[0]}")
                    if receiver_balance is None:
                        print("Receiver not found")
                        return
                    receiver_balance = receiver_balance[0]

                    # Calculate new balances
                    new_sender_balance = sender_balance - amount
                    new_receiver_balance = receiver_balance + amount

                    # Update sender's balance
                    cur.execute(update_wallet_query, (new_sender_balance, sender.user_id))
                    transaction_repo.create_transaction(sender.username, amount, 'debit-transfer', receiver_data.username)

                    # Update receiver's balance
                    cur.execute(update_wallet_query, (new_receiver_balance, receiver_data.user_id))
                    transaction_repo.create_transaction(sender.username, amount, 'credit-transfer', receiver_data.username)

                    # Commit the transaction
                    conn.commit()

                    print("Transaction completed successfully")

            except ValueError:
                print('Amount can only contain numbers')
            except Exception as e:
                print(f"Something went wrong: {e}")
                conn.rollback()
            finally:
                conn.close()

    @staticmethod
    def deposit(amount, sender):
        conn = connect_to_db()
        transaction_repo = TransactionRepositorySQL()

        update_wallet_query = """
            UPDATE wallets SET balance = %s WHERE user_id = %s;
        """

        if conn:
            try:
                amount = float(amount)
                with conn.cursor() as cur:
                    cur.execute("SELECT balance FROM wallets WHERE user_id = %s", (sender.user_id,))
                    balance = cur.fetchone()
                    if balance is None:
                        print("Wallet not found")
                        return
                    balance = balance[0]

                    new_balance = balance + amount

                    cur.execute(update_wallet_query, (new_balance, sender.user_id))
                    transaction_repo.create_transaction(sender.username, amount, 'deposit', "")
                    # Commit the transaction
                    conn.commit()

                    print("Transaction completed successfully")

            except ValueError:
                print('Amount can only contain numbers')
            except Exception as e:
                print(f"Something went wrong: {e}")
                conn.rollback()
            finally:
                conn.close()

    @staticmethod
    def withdraw(amount, sender):
        conn = connect_to_db()
        transaction_repo = TransactionRepositorySQL()

        update_wallet_query = """
            UPDATE wallets SET balance = %s WHERE user_id = %s;
        """

        if conn:
            try:
                amount = float(amount)
                with conn.cursor() as cur:
                    cur.execute("SELECT balance FROM wallets WHERE user_id = %s", (sender.user_id,))
                    balance = cur.fetchone()
                    if balance is None:
                        print("Wallet not found")
                        return
                    balance = balance[0]

                    if balance < amount:
                        print('insufficient funds')
                        return
                    
                    new_balance = balance - amount

                    cur.execute(update_wallet_query, (new_balance, sender.user_id))
                    transaction_repo.create_transaction(sender.username, amount, 'withdraw', "")
                    # Commit the transaction
                    conn.commit()

                    print("Transaction completed successfully")

            except ValueError:
                print('Amount can only contain numbers')
            except Exception as e:
                print(f"Something went wrong: {e}")
                conn.rollback()
            finally:
                conn.close()

    @staticmethod
    def view_wallet(user):
        conn = connect_to_db()

        if conn:
            try:
                with conn.cursor() as cur:
                    cur.execute("SELECT * FROM wallets WHERE user_id = %s", (user.user_id,))
                    wallet = cur.fetchone()
                    print(wallet)
                    if wallet is None:
                        print("Wallet not found")
                        return wallet
            except Exception as e:
                print(f"Something went wrong: {e}")
                conn.rollback()
            finally:
                conn.close()

    @staticmethod
    def view_balance(user):
        conn = connect_to_db()

        if conn:
            try:
                with conn.cursor() as cur:
                    cur.execute("SELECT balance FROM wallets WHERE user_id = %s", (user.user_id,))
                    balance = cur.fetchone()
                    print(balance)
                    if balance is None:
                        print("balance not available")
                        return balance
            except Exception as e:
                print(f"Something went wrong: {e}")
                conn.rollback()
            finally:
                conn.close()

class TransactionRepositorySQL:

    @staticmethod
    def create_transaction(sender, amount, Ttype, receiver):
        conn = connect_to_db()

        new_transaction_query = """
            INSERT INTO transactions (transaction_id, amount, created_at, trans_type, sender, receiver)
            VALUES (%s, %s, %s, %s, %s, %s);
        """

        if conn:
            try:
                with conn.cursor() as cur:
                    transaction_id = random.random() * 777
                    created_at = datetime.now().isoformat()

                    cur.execute(new_transaction_query, (transaction_id, amount, created_at, Ttype, sender, receiver))
                    conn.commit()
                    print("transaction created")
            except Exception as e:
                print(f"Something went wrong while creating your transaction: {e}")
                conn.rollback()
                return
            finally:
                conn.close()

    @staticmethod
    def view_transactions(username):
        conn = connect_to_db()

        search_query = """
            SELECT * FROM transactions
            WHERE (sender = %s and not trans_type = 'credit-transfer') or (receiver = %s and trans_type = 'credit-transfer')
        """

        if conn:
            try:
                with conn.cursor() as cur:
                    cur.execute(search_query, (username, username))
                    transactions = cur.fetchall()
                    print(transactions)
                    if transactions is None:
                        print("You have not carried out any transactions")
                        return transactions
            except Exception as e:
                print(f"Something went wrong: {e}")
                conn.rollback()
            finally:
                conn.close()

    @staticmethod
    def view_single_transaction(id):
        conn = connect_to_db()

        if conn:
            try:
                with conn.cursor() as cur:
                    cur.execute("SELECT * FROM transactions WHERE transaction_id = %s", (id,))
                    transaction = cur.fetchone()
                    print(transaction)
                    if transaction is None:
                        print("Transaction not found")
                        return transaction
            except Exception as e:
                print(f"Something went wrong: {e}")
                conn.rollback()
            finally:
                conn.close()





