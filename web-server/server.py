from flask import Flask, request, jsonify, render_template, redirect, url_for, session
import mysql.connector
from passlib.context import CryptContext
import settings

app = Flask(__name__, template_folder=settings.FOLDER_PATH)
app.secret_key = 'test'

# Password hashing and validation context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# function to hash a password
def hash_password(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# connect to the database
def get_db_connection():
    return mysql.connector.connect(
        host=settings.HOST,
        user=settings.USER_NAME,
        password=settings.PASSWORD,
        database=settings.DB_NAME
    )


# Routes
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/dashboard', methods=['GET'])
def dashboard():
    username = session.get('username')
    if username:
        return render_template('dashboard.html', username=username)
    return redirect(url_for('index'))

@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"status": "error", "message": "Username and password are required"}), 400

    # Enforce strong password rules
    if len(password) < 8 or not any(c.isupper() for c in password) or not any(c.islower() for c in password) or not any(c.isdigit() for c in password) or not any(c in "!@#$%^&*()-_+=" for c in password):
        return jsonify({
            "status": "error",
            "message": "Password must be at least 8 characters long, contain an uppercase letter, a lowercase letter, a number, and a special character."
        }), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT username FROM records WHERE username = %s", (username,))
        if cursor.fetchone():
            return jsonify({"status": "error", "message": "User already exists"}), 400

        hashed_password = hash_password(password)
        cursor.execute("INSERT INTO records (username, password) VALUES (%s, %s)", (username, hashed_password))
        conn.commit()
        return jsonify({"status": "success", "message": "User registered successfully"}), 201

    except mysql.connector.Error as err:
        return jsonify({"status": "error", "message": str(err)}), 500

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"status": "error", "message": "Username and password are required"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT password FROM records WHERE username = %s", (username,))
        result = cursor.fetchone()
        if result and verify_password(password, result[0]):
            session['username'] = username
            return jsonify({"status": "success", "redirect": "/dashboard"}), 200

        return jsonify({"status": "error", "message": "Invalid credentials"}), 401

    except mysql.connector.Error as err:
        return jsonify({"status": "error", "message": str(err)}), 500

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

@app.route('/logout', methods=['GET'])
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
