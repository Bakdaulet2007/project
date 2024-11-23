import sqlite3


def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()


    c.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            course TEXT,
            skills TEXT
        )
    ''')

    # Создаем таблицу для вакансий
    c.execute('''
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            company TEXT,
            description TEXT,
            category TEXT
        )
    ''')

    conn.commit()
    conn.close()


if __name__ == '__main__':
    init_db()