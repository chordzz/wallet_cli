


class Wallet:
    """A class to represent a single wallet in the system"""

    def __init__(self, wallet_obj) -> None:
        """Initialize the wallet"""

        self.wallet_id = wallet_obj.get("wallet_id")
        self.balance = wallet_obj.get("balance")
        self.user_id = wallet_obj.get("user_id")
        self.created_at = wallet_obj.get("created_at")
        self.updated_at = wallet_obj.get("updated_at")

    def __repr__(self):
        return (f"Wallet(wallet_id={self.wallet_id}, balance={self.balance}, user_id={self.user_id}, created_at={self.created_at}, updated_at={self.updated_at})")