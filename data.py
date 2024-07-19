import sqlite3

def create_db():
    conn = sqlite3.connect('botdata.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS bot_data
                      (id INTEGER PRIMARY KEY AUTOINCREMENT,
                       proxy TEXT,
                       username TEXT,
                       password TEXT,
                       email TEXT,
                       target TEXT,
                       event TEXT,
                       signal_time INTEGER,
                       start_time TEXT,
                       end_time TEXT
                   )''')
    conn.commit()
    conn.close()

def insert_data(proxy, username, password, email, target, event, signal_time, start_time, end_time):
    conn = sqlite3.connect('botdata.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO bot_data (proxy, username, password, email, target, event, signal_time, start_time, end_time) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                   (proxy, username, password, email, target, event, signal_time, start_time, end_time))
    conn.commit()
    conn.close()

def get_data():
    conn = sqlite3.connect('botdata.db')
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM bot_data")
        data = cursor.fetchall()
    except sqlite3.OperationalError:
        data = []
    finally:
        conn.close()
    return data

def get_by_id(id):
    with sqlite3.connect('botdata.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM bot_data WHERE id = ?", (id,))
        data = cursor.fetchone()
    return data



def delete_event(event_id):
    conn = sqlite3.connect('botdata.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM bot_data WHERE id = ?", (event_id,))
    conn.commit()
    conn.close()

if __name__ == '__main__':
   create_db()
