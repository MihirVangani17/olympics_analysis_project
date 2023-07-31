from flask import Flask, render_template, request, redirect, session, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

# MySQL configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Saransh' 
app.config['MYSQL_DB'] = 'flask_app'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

# Secret key for sessions
app.secret_key = 'your_secret_key'

@app.route('/')
def home():
    return render_template('lander_page.html')


@app.route('/analysis')
def analysis():
    return render_template('analysis.html')


@app.route('/prediction')
def prediction():
    return render_template('prediction.html')


@app.route('/baytickets', methods=['GET', 'POST'])
def baytickets():
    if request.method == 'POST':
        # Process signup form data and store in the database
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO users (username, email, password) VALUES (%s, %s, %s)', (username, email, password))
        mysql.connection.commit()
        cur.close()

    return render_template('baytickets.html')


# @app.route('/signup')
# def signup():
#     return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Process login form data and check credentials from the database
        username = request.form['username']
        password = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM users WHERE username = %s AND password = %s', (username, password))
        user = cur.fetchone()
        cur.close()

        if user:
            session['username'] = user['username']
            return redirect(url_for('baytickets'))

    return render_template('login.html')

# Create a route for user signup
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        connection = mysql.connection
        cursor = connection.cursor()

        # Create the users table if it doesn't exist
        cursor.execute("CREATE TABLE IF NOT EXISTS users (id INT AUTO_INCREMENT PRIMARY KEY, "
                       "username VARCHAR(255) UNIQUE NOT NULL, "
                       "email VARCHAR(255) UNIQUE NOT NULL, "
                       "password VARCHAR(255) NOT NULL)")

        # Check if the username is already taken
        cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()

        if user:
            cursor.close()
            connection.close()
            return "Username already taken. Please choose a different username."

        # Insert the new user into the database
        cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
                       (username, email, password))
        connection.commit()

        cursor.close()
        connection.close()

        # Redirect to the login page after successful signup
        return redirect(url_for('login'))

    return render_template('signup.html')

# Create a route for user login
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if 'user_id' in session:
#         return redirect(url_for('baytickets'))  # Redirect to index if already logged in

#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']

#         connection = mysql.connection
#         cursor = connection.cursor()

#         # Check if the credentials match in the database
#         cursor.execute("SELECT id FROM users WHERE username = %s AND password = %s",
#                        (username, password))
#         user = cursor.fetchone()

#         cursor.close()
#         connection.close()

#         if user:
#             # Store the user ID in the session for future authentication
#             session['user_id'] = user[0]
#             return redirect(url_for('baytickets'))  # Redirect to index page after login
#         else:
#             return "Login failed. Invalid username or password."

#     return render_template('login.html')

@app.route('/forum')
def forum():
    # Fetch and display data from the threads table in MySQL
    cur = mysql.connection.cursor()
    cur.execute('SELECT id, title, description FROM threads')  # Fetch the id, title, and description columns
    threads = cur.fetchall()
    cur.close()

    return render_template('forum.html', threads=threads)  # Pass the fetched data to the template


@app.route('/thread', methods=['GET', 'POST'])
def thread():
    if request.method == 'POST':
        # Process form data and store the new thread description and title in the database
        title = request.form['title']
        description = request.form['description']

        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO threads (title, description) VALUES (%s, %s)', (title, description))
        mysql.connection.commit()
        cur.close()

        return redirect(url_for('forum'))

    return render_template('thread.html')

@app.route('/add_thread', methods=['POST'])  # Specify 'POST' method for handling form submission
def add_thread():
    if request.method == 'POST':
        # Process form data and store the new thread description and title in the database
        title = request.form['title']
        description = request.form['description']

        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO threads (title, description) VALUES (%s, %s)', (title, description))
        mysql.connection.commit()
        cur.close()

        return redirect(url_for('forum'))

    # If accessed directly, redirect back to the thread.html page (or you can render the template here)
    return redirect(url_for('thread'))

if __name__ == '__main__':
    app.run(debug=True)
