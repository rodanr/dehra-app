import psycopg2

conn = psycopg2.connect("dbname='chat' user='rolename' password='password' host='localhost'")

cur = conn.cursor()