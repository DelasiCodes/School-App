from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a secure secret key in production

# Add a new route to submit feedback
@app.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    if 'username' in session and request.method == 'POST':
        user_id = cursor.execute('SELECT id FROM users WHERE username = ?', (session['username'],)).fetchone()[0]
        feedback_text = request.form['feedback_text']

        conn = sqlite3.connect('User.db')
        cursor = conn.cursor()

        # Submit the feedback
        cursor.execute('INSERT INTO feedback (user_id, feedback_text) VALUES (?, ?)', (user_id, feedback_text))

        conn.commit()
        conn.close()

        return redirect(url_for('dashboard'))

    return 'Invalid request'
