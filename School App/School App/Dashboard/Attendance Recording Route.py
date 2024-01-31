from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a secure secret key in production

# Add a new route to record attendance
@app.route('/record_attendance', methods=['POST'])
def record_attendance():
    if 'username' in session and request.method == 'POST':
        username = session['username']
        course_id = int(request.form['course'])
        date = request.form['date']
        present = bool(request.form.get('present', False))

        conn = sqlite3.connect('User.db')
        cursor = conn.cursor()

        # Fetch the user ID
        user_id = cursor.execute('SELECT id FROM users WHERE username = ?', (username,)).fetchone()[0]

        # Record attendance
        cursor.execute('INSERT INTO attendance (user_id, course_id, date, present) VALUES (?, ?, ?, ?)', (user_id, course_id, date, present))

        conn.commit()
        conn.close()

        return redirect(url_for('dashboard'))

    return 'Invalid request'
