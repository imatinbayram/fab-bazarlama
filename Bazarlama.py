import streamlit as st
import os

def get_db_connection():
    server = os.environ.get('DB_SERVER', '192.168.1.245')
    database = os.environ.get('DB_DATABASE', 'MikroDB_V16_04')
    username = os.environ.get('DB_USERNAME', 'MA')
    password = os.environ.get('DB_PASSWORD', 'mikro')  # Ensure this is set in the environment

    conn_str = (
        f'DRIVER={{ODBC Driver 17 for SQL Server}};'
        f'SERVER={server};'
        f'DATABASE={database};'
        f'UID={username};'
        f'PWD={password};'
        'Connection Timeout=30;'
    )
    return pyodbc.connect(conn_str)
import pyodbc

try:
    conn = get_db_connection()
    st.write("Connection successful!")
    conn.close()
except Exception as e:
    st.write(f"Error: {e}")
