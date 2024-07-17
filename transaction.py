


class Transaction:
    """A class to represent a single transaction in the system"""

    def __init__(self, trans) -> None:
        """Initialize the transaction"""

        self.id = trans.get("id")
        self.wallet_id = trans.get("wallet_id")
        self.transaction_type = trans.transaction_type
        self.amount = trans.amount
        self.receipient = trans.receipient
        self.status = trans.status
        self.created_at = trans.created_at

    def __repr__(self):
        return (f"Transaction(id={self.id}, wallet_id={self.wallet_id}, amount={self.amount}, status={self.status}, recepient={self.recepient}, created_at={self.created_at}, transaction_type={self.transaction_type})")


        