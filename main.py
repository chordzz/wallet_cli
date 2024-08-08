from time import sleep
from helpers import *
from urls import paths


def main():
    active = True

    sleep(1)
    print("App Setup Complete")

    active_user = None
    commands = {}
    counter = 1

    while active:
       
        for k, v in paths.items():
            commands[counter] = k
            counter += 1
        
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
        if user_input == '2' or user_input == '11':
            active_user = paths[commands[int(user_input)]](active_user)
        elif user_input == '12':
            active = False
        else:
            try:
                int(user_input)
            except ValueError:
                print('You need to enter a valid number')
                continue
            else:
                paths[commands[int(user_input)]](active_user)

if __name__ == '__main__':
    main()