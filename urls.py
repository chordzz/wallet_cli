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
    "wallet": wallet_view.view_wallet,
    "profile": user_view.user,
    "transaction/single": transaction_view.view_single_transaction,
    "signout": user_view.signout
}