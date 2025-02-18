from flask import Flask, request, render_template_string, jsonify
import subprocess
import os
import sqlite3
import requests
from lxml import etree

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    output = ''
    # 1 - SQL Injection
    db = sqlite3.connect("tutorial.db")
    cursor = db.cursor()
    username = ''
    password = ''
    try:
        cursor.execute("SELECT * FROM users WHERE username = '%s' AND password = '%s'" % (username, password))
    except:
        pass

    if request.method == 'POST':
        if 'username' in request.form:
            username = request.form['username']
            try:
                # Vulnerable SQL query using string interpolation
                query = "SELECT password FROM users WHERE username = '{}'".format(username)
                cursor.execute(query)
                result = cursor.fetchone()
                if result:
                    output = f"Password for {username}: {result[0]}"
                else:
                    output = "User not found."
            except Exception as e:
                output = f"SQL Error"

    return render_template_string("""
        <h1>Intentionally Insecure App</h1>
        <hr>    
    """, output=output)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False)
