import json
from flask import Flask,render_template,request,session, url_for, redirect
from flask_mysqldb import MySQL
app1 = Flask(__name__)
app1.secret_key = "secret key"
app1.config['MYSQL_HOST'] = 'localhost'
app1.config['MYSQL_USER'] = 'root'
app1.config['MYSQL_PASSWORD'] = ''
app1.config['MYSQL_DB'] = 'quanlydangnhap'
mysql = MySQL(app1)

@app1.route('/')
def index():
    if 'user' in session:
        user_name = session['user']
        return 'Logged in as ' + user_name + '<br>' + "<b><a href = '/logout'>Click here ro logout</a></b>"
    return "You are not logged in <br><a href = '/login'></b>" + "Click here to login</b></a>"

@app1.route('/login', methods=['GET', 'POST']) 
def login():
    if request.method == 'POST':
        email = request.form['inputEmail']
        password = request.form['pass']
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM dangnhap WHERE user_email=%s", [email])
        user = cur.fetchone()
        if not user:
            return render_template('login.html', message_email="Tài khoản không tồn tại")
        if int(password) != user[2]:
            return render_template('login.html', message_pass="Email hoặc mật khẩu không đúng")
        session['user'] = email
        return redirect(url_for('index'))
    return render_template('login.html')


@app1.route('/register', methods=['GET', 'POST']) 
def register():
    message = ''
    if request.method == 'POST' and 'userpassword' in request.form and 'useremail' in request.form :
        userpassword = request.form['userpassword']
        username = request.form['useremail']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM dangnnhap WHERE username = % s', (username, ))
        account = cursor.fetchone()
        if account:
            message = 'Account already exists !'
        elif not match(r'[^@]+[^@+\.[^@]+', useremail):
            message = 'Invalid email address !'
        else:
            cursor.execute('INSERT INTO dangnhap VALUES (NULL, % s, % s)', (username, userpassword, ))
            mysql.connection.commit()
            message = 'You have successfully registered !'
    elif request.method == 'POST':
        message = 'Please fill out the form !'
    return render_template('register.html', message = message)

@app1.route('/logout', methods=['GET']) 
def logout():
    for key in list(session.keys()):
        session.pop(key)
    # pop.clear()
    return redirect(url_for('index'))


if __name__ == "__main__":
    app1.run(debug=True)
