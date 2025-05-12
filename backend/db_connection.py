import mysql.connector
from mysql.connector import Error
import pyodbc

def connect_aep_portal():
    try:
        connection = mysql.connector.connect(
            host='#',
            user='#',
            password='#',
            database='#',
            charset='#'
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error connecting to aep_portal: {e}")
        return None
    
def execute_query_portal(query, params=None):
    connection = connect_aep_portal()
    if connection is None:
        return None
    cursor = connection.cursor(dictionary=True)
    cursor.execute(query, params)
    if query.strip().upper().startswith("SELECT"):
        result = cursor.fetchall()
    else:
        connection.commit()
        result = None
    cursor.close()
    connection.close()
    return result
    
def connect_aep_DB():
    server = '#'
    database = '#'
    username = '#'
    password = '#'
    
    try:
        conn = pyodbc.connect(
            f'DRIVER={{ODBC Driver 17 for SQL Server}};'
            f'SERVER={server};'
            f'DATABASE={database};'
            f'UID={username};'
            f'PWD={password}'
        )
        return conn
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None