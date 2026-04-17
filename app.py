from flask import Flask, request, redirect, session, render_template_string
import sqlite3
import bcrypt

app = Flask(__name__)
app.secret_key = 'secret123'   # change in real project

# Database setup
def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (username TEXT, password BLOB)''')
    conn.commit()
    conn.close()

init_db()

# HTML Template
HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Auth System</title>
    <style>
        body { font-family: Arial; padding: 20px; }
        input, button { padding: 10px; margin: 5px; }
    </style>
</head>
<body>

<h2>🔐 Secure Authentication System</h2>

{% if session.get('user') %}
    <h3>Welcome, {{ session['user'] }}</h3>
    <a href="/logout">Logout</a>
{% else %}

<h3>Signup</h3>
<form method="POST" action="/signup">
    <input type="text" name="username" placeholder="Username" required>
    <input type="password" name="password" placeholder="Password" required>
    <button type="submit">Signup</button>
</form>

<h3>Login</h3>
<form method="POST" action="/login">
    <input type="text" name="username" placeholder="Username" required>
    <input type="password" name="password" placeholder="Password" required>
    <button type="submit">Login</button>
</form>

{% endif %}

</body>
</html>
"""

# Home
@app.route('/')
def home():
    return render_template_string(HTML)

# Signup
@app.route('/signup', methods=['POST'])
def signup():
    username = request.form['username']
    password = request.form['password']

    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("INSERT INTO users VALUES (?, ?)", (username, hashed))
    conn.commit()
    conn.close()

    return redirect('/')

# Login
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=?", (username,))
    user = c.fetchone()
    conn.close()

    if user and bcrypt.checkpw(password.encode('utf-8'), user[1]):
        session['user'] = username

    return redirect('/')

# Logout
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
