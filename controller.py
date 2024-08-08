
from helpers import *


def setup_postgres():

    conn = connect_to_db()


    users_table_schema = [
        ("name", "VARCHAR"),
        ("email", "VARCHAR"),
        ("phone", "VARCHAR"),
        ("username", "VARCHAR"),
        ("password", "VARCHAR"),
        ("user_id", "VARCHAR"),
        ("created_at", "TIMESTAMP")
    ]

    wallets_table_schema = [
        ("wallet_id", "VARCHAR"),
        ("balance", "FLOAT"),
        ("created_at", "TIMESTAMP"),
        ("updated_at", "TIMESTAMP"),
        ("user_id", "VARCHAR"),   
    ]

    transactions_table_schema = [
        ("transaction_id", "VARCHAR"),
        ("amount", "FLOAT"),
        ("created_at", "TIMESTAMP"),
        ("trans_type", "VARCHAR"),
        ("sender", "VARCHAR"),   
        ("receiver", "VARCHAR"),   
    ]

    setup_table_flow("users", users_table_schema)
    setup_table_flow("wallets", wallets_table_schema)
    setup_table_flow("transactions", transactions_table_schema)
