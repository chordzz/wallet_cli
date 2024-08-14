import json
from psycopg2 import connect, sql
import hashlib


################### FILE DB ###########################
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

###############################################################



################ POSTGRESQL ################################


def hash_password(password):
   password_bytes = password.encode('utf-8')
   hash_object = hashlib.sha256(password_bytes)
   return hash_object.hexdigest()


connection_parameters = {
    "database":"wallet-cli-ai",
    "host":"localhost",
    "user":"postgres",
    "password":"postgres",
    "port":"5432"
}

def connect_to_db():
    try:
        conn = connect(**connection_parameters)
        print("Connected to the database")
        return conn
    except Exception as e:
        print("Unable to connect to the database")
        print(e)

def check_table(table_name):
    conn = connect_to_db()
    
    check_table_query = """
        SELECT EXISTS (
            SELECT FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_name = %s
        );
        """
    
    try:
        with conn.cursor() as cur:
            cur.execute(check_table_query, (table_name))
            result = cur.fetchone()
            return result
    except Exception as e:
        print(f"Error checking if table exists: {e}")
        return False
    finally:
        conn.close()
    
def create_table(name, columns):
    conn = connect_to_db()

    fields = []
    for col in columns:
        fields.append(sql.SQL("{} {}").format(sql.Identifier(col[0]), sql.SQL(col[1])))

    query = sql.SQL("CREATE TABLE {tbl_name} ({fields});").format(
        tbl_name=sql.Identifier(name),
        fields=sql.SQL(', ').join(fields)
    )

    try:
        with conn.cursor() as cur:
            cur.execute(query)
            conn.commit()
            print(f"Table '{name}' created successfully.")
    except Exception as e:
        print(f"Error creating table '{name}': {e}")
    finally:
        conn.close()

def setup_table_flow(table_name, columns):
    if not check_table(table_name):
        create_table(table_name, columns)
    else:
        print(f"Table {table_name} already exists.")


