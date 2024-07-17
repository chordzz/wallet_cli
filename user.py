

class User:
    """A class to represent a single user in the system"""

    def __init__(self, e_user) -> None:
        """Initialize the user"""

        self.name = e_user.get("name")
        self.username = e_user.get("username")
        self.phone = e_user.get("phone")
        self.email = e_user.get("email")
        self.created_at = e_user.get("created_at")
        self.user_id = e_user.get("user_id")
        self.password = e_user.get("password")
        self.status = e_user.get("status", "active")

    def __repr__(self):
        return (f"User(user_id={self.user_id}, username={self.username}, email={self.email}, phone={self.phone}, name={self.name}, created_at={self.created_at}, status={self.status})")
        