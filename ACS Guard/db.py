import pymysql

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "Myservermybestfriend09941991294",
    "database": "innovex_2026"
}

def get_connection():
    return pymysql.connect(
        host=DB_CONFIG["host"],
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
        database=DB_CONFIG["database"],
        cursorclass=pymysql.cursors.DictCursor
    )

# Check employee login
def verify_login(email, password):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM employees WHERE gmail = %s AND pass = %s", (email, password))
    result = cursor.fetchone()
    conn.close()
    return result

