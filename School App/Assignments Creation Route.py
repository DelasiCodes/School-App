from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a secure secret key in production

# Add a new route to create assignments
@app.route('/create_assignment', methods=['POST'])
def create_assignment():
    if 'username' in session and request.method == 'POST':
        user_id = cursor.execute('SELECT id FROM users WHERE username = ?', (session['username'],)).fetchone()[0]
        assignment_name = request.form['assignment_name']
        assignment_due_date = request.form['assignment_due_date']
        assignment_description = request.form['assignment_description']

        conn = sqlite3.connect('User.db')
        cursor = conn.cursor()

        # Create the assignment
        cursor.execute('INSERT INTO assignments (user_id, assignment_name, assignment_due_date, assignment_description) VALUES (?, ?, ?, ?)', (user_id, assignment_name, assignment_due_date, assignment_description))

        conn.commit()
        conn.close()

        return redirect(url_for('dashboard'))

    return 'Invalid request'
