import json

def read_from_db(path):
    # Load in the users DB, create it if it doesn't exist
    try:
        users_fr = open(path, 'r')
        user_dicts = json.load(users_fr)
        return user_dicts
    except FileNotFoundError:
        print("DB not found, creating one now")
        open(path, 'x').close()
    except json.decoder.JSONDecodeError:
        print("DB is empty or corrupted, reinitializing")
        print("Reinitialization complete")

def write_to_db(path, data):
    """Function to write to any DB"""
    w = open(path, 'w')
    w.write(json.dumps(data, indent=4))
    w.close()