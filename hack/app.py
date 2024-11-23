from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)


# Инициализация базы данных
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    # Создаем таблицу для студентов, если она не существует
    c.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            course TEXT,
            skills TEXT
        )
    ''')
    conn.commit()
    conn.close()


# Главная страница, отображающая список студентов
@app.route('/')
def index():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()


    c.execute('SELECT * FROM students')
    students = c.fetchall()

    conn.close()
    return render_template('index.html', students=students)



@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if request.method == 'POST':
        name = request.form['name']
        course = request.form['course']
        skills = request.form['skills']

        conn = sqlite3.connect('database.db')
        c = conn.cursor()


        c.execute('INSERT INTO students (name, course, skills) VALUES (?, ?, ?)', (name, course, skills))
        conn.commit()
        conn.close()

        return redirect('/')

    return render_template('profile.html')



if __name__ == '__main__':
    init_db()
    app.run(debug=True)

@app.route('/')
def index():
    # Получаем параметры категории и поиска из URL
    category = request.args.get('category')  # Фильтр по категории
    search_query = request.args.get('search')  # Поиск по названию вакансии

    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    # Строим SQL-запрос с фильтрацией по категории и поиском по названию
    query = 'SELECT * FROM jobs WHERE 1=1'  # Начинаем с базового запроса
    params = []

    if category:
        query += ' AND category = ?'  # Фильтрация по категории
        params.append(category)
    
    if search_query:
        query += ' AND title LIKE ?'  # Поиск по названию вакансии
        params.append(f'%{search_query}%')

    c.execute(query, params)
    jobs = c.fetchall()

    conn.close()
    return render_template('index.html', jobs=jobs, category=category, search_query=search_query)
