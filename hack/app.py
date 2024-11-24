from flask import Flask, render_template, request, redirect, session, flash
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'


# Инициализация базы данных
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    # Создаем таблицу для пользователей
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')

    # Создаем таблицу для вакансий
    c.execute('''
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            company TEXT NOT NULL,
            description TEXT NOT NULL,
            category TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()


# Главная страница
@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect('/login')

    return render_template('index.html', username=session['username'])


# Страница регистрации
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash("Passwords do not match!", "danger")
            return redirect('/register')

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?)', (username, email, hashed_password))
        conn.commit()
        conn.close()

        flash("Registration successful! You can now log in.", "success")
        return redirect('/login')

    return render_template('register.html')


# Логин
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect('database.db')
        c = conn.cursor()

        c.execute('SELECT * FROM users WHERE email = ?', (email,))
        user = c.fetchone()

        conn.close()

        if user and check_password_hash(user[3], password):
            session['user_id'] = user[0]
            session['username'] = user[1]
            return redirect('/')
        else:
            flash("Invalid email or password.", "danger")
            return redirect('/login')

    return render_template('login.html')


# Добавление вакансии
@app.route('/add_job', methods=['GET', 'POST'])
def add_job():
    if request.method == 'POST':
        title = request.form['title']
        company = request.form['company']
        description = request.form['description']
        category = request.form['category']

        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute('INSERT INTO jobs (title, company, description, category) VALUES (?, ?, ?, ?)',
                  (title, company, description, category))
        conn.commit()
        conn.close()

        flash("Job added successfully!", "success")
        return redirect('/')

    return render_template('add_job.html')


# Вакансии
@app.route('/vacancies')
def vacancies():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    c.execute('SELECT * FROM jobs')
    jobs = c.fetchall()

    conn.close()

    return render_template('vacancies.html', jobs=jobs)

@app.route('/logout')
def logout():
    session.clear()  # Очищаем сессию (выход из системы)
    flash("You have been logged out.", "info")
    return redirect('/login')  # Перенаправляем на страницу вход
if __name__ == '__main__':
    init_db()
    app.run(debug=True)