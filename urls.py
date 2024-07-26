from views import *

user_view = UserView()
wallet_view = WalletView()
transaction_view = TransactionView()

paths = {
    "signup": user_view.signup,
    "signin": user_view.signin,
    "deposit": wallet_view.deposit,
    "withdraw": wallet_view.withdraw,
    "send": wallet_view.send,
    "balance": wallet_view.view_balance,
    "transactions": transaction_view.view_transactions,
    "transaction/single": transaction_view.view_single_transaction,
    "profile": user_view.user,
    "wallet": wallet_view.view_wallet,
    "signout": user_view.signout
}