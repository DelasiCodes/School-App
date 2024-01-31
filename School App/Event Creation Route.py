from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a secure secret key in production

# Add a new route to create events
@app.route('/create_event', methods=['POST'])
def create_event():
    if 'username' in session and request.method == 'POST':
        user_id = cursor.execute('SELECT id FROM users WHERE username = ?', (session['username'],)).fetchone()[0]
        event_name = request.form['event_name']
        event_date = request.form['event_date']
        event_description = request.form['event_description']

        conn = sqlite3.connect('User.db')
        cursor = conn.cursor()

        # Create the event
        cursor.execute('INSERT INTO events (user_id, event_name, event_date, event_description) VALUES (?, ?, ?, ?)', (user_id, event_name, event_date, event_description))

        conn.commit()
        conn.close()

        return redirect(url_for('dashboard'))

    return 'Invalid request'
