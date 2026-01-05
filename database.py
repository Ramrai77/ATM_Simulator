import mysql.connector

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="password",
        database="atm_system"
    )


# ---------- USER ----------
def register_user(user_id, pin):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (user_id, pin, balance) VALUES (%s, %s, %s)",
            (user_id, pin, 0)
        )
        conn.commit()
        return True
    except mysql.connector.Error:
        return False
    finally:
        conn.close()


def login_user(user_id, pin):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT balance FROM users WHERE user_id=%s AND pin=%s",
        (user_id, pin)
    )
    result = cursor.fetchone()
    conn.close()
    return result


def update_balance(user_id, balance):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE users SET balance=%s WHERE user_id=%s",
        (balance, user_id)
    )
    conn.commit()
    conn.close()


# ---------- TRANSACTIONS ----------
def add_transaction(user_id, action, amount):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO transactions (user_id, action, amount) VALUES (%s, %s, %s)",
        (user_id, action, amount)
    )
    conn.commit()
    conn.close()


def get_transactions(user_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT action, amount, created_at FROM transactions WHERE user_id=%s",
        (user_id,)
    )
    data = cursor.fetchall()
    conn.close()
    return data
