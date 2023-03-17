import secrets
import time
import mysql.connector
from mysql.connector import errorcode
import xml.etree.ElementTree as ET

TOKEN_VALIDITY_SECONDS = 24 * 60 * 60


def _get_db_config():
    tree = ET.parse("xml/tokenApi.xml")
    root = tree.getroot()

    config = {
        "user": root.find("user").text,
        "password": root.find("password").text,
        "host": root.find("host").text,
        "database": root.find("database").text
    }

    return config


def _get_db_connection():
    config = _get_db_config()

    try:
        return mysql.connector.connect(**config)
    except mysql.connector.Error as err:
        print(f"Failed to connect to the database: {err}")
        return None


def create_token(client_key):
    db_connection = _get_db_connection()
    if db_connection is None:
        return None

    cursor = db_connection.cursor()
    cursor.execute("SELECT * FROM GH_TOKEN_MST WHERE CLIENT_KEY = %s", (client_key,))

    if cursor.rowcount == 0:
        return None

    token_id = secrets.token_hex(32)
    expiry_time = int(time.time()) + TOKEN_VALIDITY_SECONDS

    cursor.execute("INSERT INTO GH_TOKEN_MST (TOKEN_ID, CLIENT_KEY, EXPIRY_TIME) VALUES (%s, %s, %s)",
                   (token_id, client_key, expiry_time))
    db_connection.commit()

    cursor.close()
    db_connection.close()

    return token_id


def verify_token(token_id):
    db_connection = _get_db_connection()
    if db_connection is None:
        return None

    cursor = db_connection.cursor()
    cursor.execute("SELECT * FROM GH_TOKEN_MST WHERE TOKEN_ID = %s", (token_id,))

    if cursor.rowcount == 0:
        return None

    result = cursor.fetchone()
    client_key = result[0]
    expiry_time = result[2]

    if expiry_time < int(time.time()):
        cursor.execute("DELETE FROM GH_TOKEN_MST WHERE TOKEN_ID = %s", (token_id,))
        db_connection.commit()

