import psycopg2
from  psycopg2 import DatabaseError

def get_conection(): 
    DB_HOST = "localhost"
    DB_NAME = "final_teamray"
    DB_USER = "postgres"
    DB_PASS = "2004"
 
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
    return conn