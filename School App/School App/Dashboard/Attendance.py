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

        # Fetch courses for the user
        if user_type == 'student':
            cursor.execute('SELECT id, course_name FROM courses')
            courses = [{'id': row[0], 'course_name': row[1]} for row in cursor.fetchall()]
            # Fetch attendance records for the student
            student_id = cursor.execute('SELECT id FROM users WHERE username = ?', (username,)).fetchone()[0]
            attendance_records = cursor.execute('SELECT course_id, date, present FROM attendance WHERE user_id = ?', (student_id,)).fetchall()
        elif user_type == 'teacher':
            # Fetch courses for the teacher
            cursor.execute('SELECT id, course_name FROM courses')
            courses = [{'id': row[0], 'course_name': row[1]} for row in cursor.fetchall()]
            # Fetch attendance records for the teacher's courses
            teacher_id = cursor.execute('SELECT id FROM users WHERE username = ?', (username,)).fetchone()[0]
            attendance_records = cursor.execute('SELECT course_id, date, present FROM attendance WHERE user_id = ?', (teacher_id,)).fetchall()
        else:
            # Handle other user types if needed
            courses = []
            attendance_records = []

        conn.close()

        return render_template('dashboard.html', username=username, user_type=user_type, courses=courses, attendance_records=attendance_records)

    return 'You are not logged in<br><a href="/login">Login</a>'
