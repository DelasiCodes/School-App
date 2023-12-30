from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a secure secret key in production

# Add a new route to add resources
@app.route('/add_resource', methods=['POST'])
def add_resource():
    if 'username' in session and request.method == 'POST':
        user_id = cursor.execute('SELECT id FROM users WHERE username = ?', (session['username'],)).fetchone()[0]
        resource_name = request.form['resource_name']
        resource_description = request.form['resource_description']
        resource_link = request.form['resource_link']

        conn = sqlite3.connect('User.db')
        cursor = conn.cursor()

        # Add the resource
        cursor.execute('INSERT INTO resources (user_id, resource_name, resource_description, resource_link) VALUES (?, ?, ?, ?)', (user_id, resource_name, resource_description, resource_link))

        conn.commit()
        conn.close()

        return redirect(url_for('dashboard'))

    return 'Invalid request'
