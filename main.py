from time import sleep
from helpers import *
from urls import paths


def main():
    active = True
    # user_db_path = "data/users.json"
    # wallet_db_path = "data/wallets.json"
    # transactions_db_path = "data/transactions.json"

    sleep(1)
    print("Welcome to your HB wallet...")
    print("please wait while we setup your app")

    # users = read_from_db(user_db_path)
    # wallets = read_from_db(wallet_db_path)
    # transactions = read_from_db(transactions_db_path)

    sleep(1)
    print("App Setup Complete")

    active_user = None

    while active:
        sleep(1)

        print("\nEnter the corresponding numbers to perform an action.")
        user_input = input("1. Create Account\n"
                            "2. Sign-in to your Account\n"
                            "3. Deposit Money \n"
                            "4. Withdraw Money \n"
                            "5. Send Money \n"
                            "6. Check Balance \n"
                            "7. My Transactions \n"
                            "8. My wallet\n"
                            "9. My Profile\n"
                            "10. View single transaction\n"
                            "11. Sign out \n"
                            "12. Exit App \n"
                            )
        
        if user_input == '1':
            paths['signup']()
        elif user_input == '2':
            if active_user:
                print("You are logged in already, logout to perform this action")
            else:
                active_user = paths['signin']()
        elif user_input == '3':
            if not active_user:
                print("You need to be logged in to carry out this action")
            else:
                paths['deposit'](active_user['user_id'], active_user['username'])
        elif user_input == '4':
            if not active_user:
                print("You need to be logged in to carry out this action")
            else:
                paths['withdraw'](active_user['user_id'], active_user['username'])
        elif user_input == '5':
            if not active_user:
                print("You need to be logged in to carry out this action")
            else:
                paths['send'](active_user['user_id'], active_user['username'])
        elif user_input == '6':
            if not active_user:
                print("You need to be logged in to carry out this action")
            else:
                paths['balance'](active_user['user_id'])
        elif user_input == '7':
            if not active_user:
                print("You need to be logged in to carry out this action")
            else:
                paths['transactions'](active_user['username'])
        elif user_input == '8':
            if not active_user:
                print("You need to be logged in to carry out this action")
            else:
                paths['wallet'](active_user['user_id'])
        elif user_input == '9':
            if not active_user:
                print("You need to be logged in to carry out this action")
            else:
                paths['profile']()
        elif user_input == '10':
            if not active_user:
                print("You need to be logged in to carry out this action")
            else:
                paths['transaction/single']()
        elif user_input == '11':
            if not active_user:
                print("You need to be logged in to carry out this action")
            else:
                active_user = paths['signout']()
        elif user_input == '12':
            print('Goodbye...')
            active = False
            
        



if __name__ == '__main__':
    main()