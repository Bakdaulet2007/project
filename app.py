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