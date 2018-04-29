from flask import Flask,render_template, request
from flask_mysqldb import MySQL
app = Flask(__name__)
app.config['MYSQL_HOST'] = 'sql9.freemysqlhosting.net'
app.config['MYSQL_USER'] = 'sql9233071'
app.config['MYSQL_PASSWORD'] = '1uXgh92Fwi'
app.config['MYSQL_DB'] = 'sql9233071'
mysql = MySQL(app)

msg = {0:"The username and password combination supplied does not match any accounts on record. Please try to login again or register if you are a new user.", 1:"Please login using the fields below."}



# valid_user(usr,psw):
#     cur = mysql.connection.cursor()

# @app.route(/register, methods=['GET', 'POST'])
# def register():
#     cur = mysql.connection.cursor()

#         ans = cur.fetchall()



@app.route('/login', methods=['GET', 'POST'])
def login():
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        username =  request.form['usr']
        password = request.form['psw']
        print username
        print password
        string = '''SELECT userid FROM USERS where uname='''+"'" +username+"'"
        print string
        cur.execute(string)
        ans = cur.fetchall()
        if len(ans) != 0:
            return render_template('timeline.html')
        else:
            return render_template('login.html', display = msg[0])


    return render_template('login.html', display = msg[1])

@app.route('/register', methods=['GET', 'POST'])
def register():
    conn = mysql.connection
    cur = conn.cursor()
    id_max = 0
    cur.execute('''SELECT userid FROM USERS''')
    for id in cur.fetchall():
        if id[0] > id_max:
            id_max = int(id[0]) + 1
    if request.method == 'POST':
        username =  request.form['usr']
        password = request.form['psw']
        print username
        print password
        string = '''INSERT INTO USERS ( USERID, UNAME, PASSWORD) VALUES''' + "(" +  "'" + str(id_max) + "'" + "," + "'" + username + "'" + "," + "'" + password + "'" + ")"
        print string
        try:
            cur.execute(string)
            conn.commit()
        except mysql.connection.IntegrityError as err:
            print("Error: {}".format(err))
            return render_template('register.html', display = "That username is already taken. Please try again.")
        return render_template('timeline.html')
        # result = cur.fetchall()
        # print result
    return render_template('register.html')

@app.route('/', methods=['GET', 'POST'])
def index():
    cur = mysql.connection.cursor()


    return render_template('index.html')
if __name__ == "__main__":
    app.run(use_reloader=True)
