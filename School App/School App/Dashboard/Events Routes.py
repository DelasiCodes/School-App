from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a secure secret key in production

# Update the /dashboard route
@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        username = session['username']

        conn = sqlite3.connect('User.db')
        cursor = conn.cursor()
        cursor.execute('SELECT user_type FROM users WHERE username = ?', (username,))
        user_type = cursor.fetchone()[0]

        # Fetch events for the user
        user_id = cursor.execute('SELECT id FROM users WHERE username = ?', (username,)).fetchone()[0]
        events = cursor.execute('SELECT * FROM events WHERE user_id = ? ORDER BY event_date', (user_id,)).fetchall()

        # Fetch other relevant information based on user type

        conn.close()

        return render_template('dashboard.html', username=username, user_type=user_type, events=events) # other relevant data

    return 'You are not logged in<br><a href="/login">Login</a>'
