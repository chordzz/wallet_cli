class Transaction:
    """A class to represent a single transaction in the system"""

    def __init__(self, sender, amount, Ttype, transaction_id, created_at, receiver="") -> None:
        """Initialize the transaction"""
        self.transaction_id = transaction_id
        self.created_at = created_at
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.Ttype = Ttype

    def to_dict(self):
        return {
            "transaction_id": self.transaction_id,
            "created_at": self.created_at,
            "sender": self.sender,
            "receiver": self.receiver,
            "amount": self.amount,
            "Ttype": self.Ttype
        }

    # def __repr__(self): return (f"Transaction(id={self.id}, wallet_id={self.wallet_id}, amount={self.amount},
    # status={self.status}, recepient={self.recepient}, created_at={self.created_at}, transaction_type={
    # self.transaction_type})")


