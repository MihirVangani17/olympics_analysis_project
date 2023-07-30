from flask import Flask, render_template, request, redirect, session, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

# MySQL configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'ProjectGFG' 
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
        # Process signup form data and store in database
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO users (username, email, password) VALUES (%s, %s, %s)', (username, email, password))
        mysql.connection.commit()
        cur.close()

    return render_template('baytickets.html')


@app.route('/signup')
def signup():
    return render_template('signup.html')


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


@app.route('/forum')
def forum():
    # Fetch and display descriptions from the threads table in MySQL
    cur = mysql.connection.cursor()
    cur.execute('SELECT description FROM threads')
    descriptions = cur.fetchall()
    cur.close()

    return render_template('forum.html', descriptions=descriptions)


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


if __name__ == '__main__':
    app.run(debug=True)
