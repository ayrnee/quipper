from flask import Flask,render_template, request
from flask_mysqldb import MySQL
app = Flask(__name__)
app.config['MYSQL_HOST'] = 'sql9.freemysqlhosting.net'
app.config['MYSQL_USER'] = 'sql9233071'
app.config['MYSQL_PASSWORD'] = '1uXgh92Fwi'
app.config['MYSQL_DB'] = 'sql9233071'
mysql = MySQL(app)

# valid_user(usr,psw):
#     cur = mysql.connection.cursor()


@app.route('/login', methods=['GET', 'POST'])
def login():
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        username =  request.form['usr']
        password = request.form['psw']
        print username
        print password
        str = '''SELECT userid FROM USERS where uname='''+"'" +username+"'"
        print str
        cur.execute(str)
        ans = cur.fetchall()
        print ans

        return render_template('login.html')

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    cur = mysql.connection.cursor()
    cur.execute('''SELECT userid FROM USERS''')
    uname = cur.fetchall()
    print uname
    return render_template('register.html')

@app.route('/', methods=['GET', 'POST'])
def index():

    return render_template('index.html')
if __name__ == "__main__":
    app.run(use_reloader=True)
