import psycopg2  # Importing the psycopg2 module to interact with PostgreSQL databases

# Establishing a connection to the PostgreSQL database
connection = psycopg2.connect(
    dbname="postgres",  # Name of the database
    user="postgres",  # Username for the database
    password="postgres",  # Password for the database
    host="localhost",  # Hostname of the database server
    port="5432"  # Port number for the database server
)

# Creating a cursor object to interact with the database
dbCursor = connection.cursor()

def alter_table():
    """
    Alters the user_logins table to change the app_version column type to varchar.
    """
    dbCursor.execute("""
        ALTER TABLE user_logins
        ALTER COLUMN app_version TYPE varchar(32)
    """)

def insert_into_postgres(userData: tuple):
    """
    Inserts processed user data into the Postgres database.
    Args:
    userData (tuple): The processed user data to be inserted.
    """
    dbCursor.execute("""
        INSERT INTO user_logins (user_id, device_type, masked_ip, masked_device_id, locale, app_version, create_date)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, userData)

def commit_and_close():
    """
    Commits the current transaction and closes the database connection.
    """
    connection.commit()  # Commit the current transaction
    dbCursor.close()  # Close the cursor
    connection.close()  # Close the database connection
