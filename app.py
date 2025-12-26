from flask import Flask, render_template, request, jsonify
from flask_mysqldb import MySQL
import os
import time
import MySQLdb

app = Flask(__name__)

# 🔹 MySQL Configuration (IMPORTANT)
app.config['MYSQL_HOST'] = os.environ.get('MYSQL_HOST', 'mysql')
app.config['MYSQL_USER'] = os.environ.get('MYSQL_USER', 'admin')
app.config['MYSQL_PASSWORD'] = os.environ.get('MYSQL_PASSWORD', 'admin')
app.config['MYSQL_DB'] = os.environ.get('MYSQL_DB', 'myDb')

# Initialize MySQL
mysql = MySQL(app)

# 🔹 Safe DB initialization with retry
def init_db():
    retries = 10
    while retries > 0:
        try:
            cur = mysql.connection.cursor()
            cur.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INT AUTO_INCREMENT PRIMARY KEY,
                message TEXT
            );
            """)
            mysql.connection.commit()
            cur.close()
            print("✅ Database initialized")
            return
        except MySQLdb.OperationalError:
            print("⏳ Waiting for MySQL...")
            retries -= 1
            time.sleep(3)

    raise Exception("❌ MySQL not reachable")

# 🔹 Run DB init AFTER Flask starts
@app.before_first_request
def initialize_database():
    

@app.route('/')
def hello():
    init_db()
    cur = mysql.connection.cursor()
    cur.execute('SELECT message FROM messages')
    messages = cur.fetchall()
    cur.close()
    return render_template('index.html', messages=messages)

@app.route('/submit', methods=['POST'])
def submit():
    new_message = request.form.get('new_message')
    cur = mysql.connection.cursor()
    cur.execute('INSERT INTO messages (message) VALUES (%s)', (new_message,))
    mysql.connection.commit()
    cur.close()
    return jsonify({'message': new_message})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

