import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="ara_db",
    user="postgres",
    password="Badri@123"
)

cur = conn.cursor()

cur.execute("SELECT current_database();")

print(cur.fetchone())

cur.close()
conn.close()