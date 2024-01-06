from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a secure secret key in production

# Create an SQLite database and a users table (run this only once)
conn = sqlite3.connect('User.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        password TEXT NOT NULL,
        user_type TEXT NOT NULL
    )
''')
conn.commit()
conn.close()

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        username = session['username']

        conn = sqlite3.connect('User.db')
        cursor = conn.cursor()
        cursor.execute('SELECT user_type FROM users WHERE username = ?', (username,))
        user_type = cursor.fetchone()[0]

        if user_type == 'student':
            # Fetch assignments for the student
            user_id = cursor.execute('SELECT id FROM users WHERE username = ?', (username,)).fetchone()[0]
            assignments = cursor.execute('SELECT * FROM assignments WHERE user_id = ? ORDER BY assignment_due_date', (user_id,)).fetchall()

            # Fetch attendance records for the student
            attendance_records = cursor.execute('SELECT course_id, date, present FROM attendance WHERE user_id = ?', (user_id,)).fetchall()

            # Fetch events for the student
            events = cursor.execute('SELECT * FROM events WHERE user_id = ? ORDER BY event_date', (user_id,)).fetchall()

            # Fetch other relevant information for students

            conn.close()

            return render_template('dashboard.html', username=username, user_type=user_type, assignments=assignments, attendance_records=attendance_records, events=events)  # other relevant data

        elif user_type == 'teacher':
            # Fetch courses for the teacher
            courses = cursor.execute('SELECT id, course_name FROM courses').fetchall()

            # Fetch attendance records for the teacher's courses
            teacher_id = cursor.execute('SELECT id FROM users WHERE username = ?', (username,)).fetchone()[0]
            attendance_records = cursor.execute('SELECT course_id, date, present FROM attendance WHERE user_id = ?', (teacher_id,)).fetchall()

            # Fetch events for the teacher
            events = cursor.execute('SELECT * FROM events WHERE user_id = ? ORDER BY event_date', (teacher_id,)).fetchall()

            # Fetch other relevant information for teachers

            conn.close()

            return render_template('dashboard.html', username=username, user_type=user_type, courses=courses, attendance_records=attendance_records, events=events)  # other relevant data

        else:
            # Handle other user types if needed
            conn.close()
            return 'Unsupported user type'

    return 'You are not logged in<br><a href="/login">Login</a>'

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
