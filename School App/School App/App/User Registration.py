from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a secure secret key in production

# Modify the user registration part
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_type = request.form['user_type']
        
        conn = sqlite3.connect('User.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (username, password, user_type) VALUES (?, ?, ?)', (username, password, user_type))
        
        if user_type == 'student':
            # Assign some courses to the student
            courses = [('Math',), ('English',), ('Science',)]
            cursor.executemany('INSERT INTO courses (course_name) VALUES (?)', courses)
            
            # Assign grades for the student in each course
            student_id = cursor.lastrowid
            grades = [(student_id, 1, 90), (student_id, 2, 85), (student_id, 3, 92)]
            cursor.executemany('INSERT INTO grades (user_id, course_id, grade) VALUES (?, ?, ?)', grades)
        
        conn.commit()
        conn.close()
        
        return redirect(url_for('login'))
    
    return render_template('register.html')
