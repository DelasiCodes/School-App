from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

# Modify the database schema
conn = sqlite3.connect('User.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS feedback (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        feedback_text TEXT,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
''')
conn.commit()
conn.close()
