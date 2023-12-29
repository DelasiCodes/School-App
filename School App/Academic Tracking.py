from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a secure secret key in production

# Update the home route
@app.route('/')
def home():
    if 'username' in session:
        username = session['username']

        conn = sqlite3.connect('User.db')
        cursor = conn.cursor()
        cursor.execute('SELECT user_type FROM users WHERE username = ?', (username,))
        user_type = cursor.fetchone()[0]

        # Fetch courses for the user
        if user_type == 'student':
            cursor.execute('SELECT id, course_name FROM courses')
            courses = [{'id': row[0], 'course_name': row[1]} for row in cursor.fetchall()]

            # Fetch grades for the student
            cursor.execute('SELECT course_id, grade FROM grades WHERE user_id = (SELECT id FROM users WHERE username = ?)', (username,))
            grades = {row[0]: {'grade': row[1]} for row in cursor.fetchall()}
        elif user_type == 'teacher':
            # Fetch courses for the teacher
            cursor.execute('SELECT course_name FROM courses')
            courses = [{'course_name': row[0]} for row in cursor.fetchall()]
            grades = {}

        conn.close()

        return render_template('dashboard.html', username=username, user_type=user_type, courses=courses, grades=grades)

    return 'You are not logged in<br><a href="/login">Login</a>'
