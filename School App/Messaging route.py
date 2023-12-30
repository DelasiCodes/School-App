from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a secure secret key in production

# Add a new route to send messages
@app.route('/send_message', methods=['POST'])
def send_message():
    if 'username' in session and request.method == 'POST':
        sender_id = cursor.execute('SELECT id FROM users WHERE username = ?', (session['username'],)).fetchone()[0]
        recipient_id = int(request.form['recipient'])
        message_text = request.form['message']

        conn = sqlite3.connect('User.db')
        cursor = conn.cursor()

        # Record the message
        cursor.execute('INSERT INTO messages (sender_id, recipient_id, message) VALUES (?, ?, ?)', (sender_id, recipient_id, message_text))

        conn.commit()
        conn.close()

        return redirect(url_for('dashboard'))

    return 'Invalid request'
