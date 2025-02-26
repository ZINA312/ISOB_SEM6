import sqlite3

def create_database():
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE users (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')

    cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', 
                 ('admin', 'secure_password'))
    conn.commit()
    return conn

# Уязвимая функция 
def unsafe_login(conn, username, password):
    cursor = conn.cursor()
    # ОПАСНО: конкатенация строк напрямую
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    cursor.execute(query)
    return cursor.fetchone() is not None

# Безопасная функция с параметризованным запросом
def safe_login(conn, username, password):
    cursor = conn.cursor()
    # Безопасно: использование параметризованного запроса
    cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', 
                 (username, password))
    return cursor.fetchone() is not None

def demonstration():
    conn = create_database()
    
    evil_password = "' OR '1'='1"  
    
    print("=== Уязвимая проверка ===")
    if unsafe_login(conn, 'admin', evil_password):
        print("Успешный взлом! (SQL-инъекция сработала)")
    else:
        print("Вход отклонен")
        
    print("\n=== Безопасная проверка ===")
    if safe_login(conn, 'admin', evil_password):
        print("Вход выполнен")
    else:
        print("SQL-инъекция предотвращена!")

if __name__ == "__main__":
    demonstration()