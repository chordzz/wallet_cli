from helpers import *
from repositories import *

print(UserRepositorySQL.get_user_by_username('iferrum').to_dict())