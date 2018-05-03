from flask import Flask,render_template, request
from flask_mysqldb import MySQL
app = Flask(__name__)
app.config['MYSQL_HOST'] = 'sql9.freemysqlhosting.net'
app.config['MYSQL_USER'] = 'sql9233071'
app.config['MYSQL_PASSWORD'] = '1uXgh92Fwi'
app.config['MYSQL_DB'] = 'sql9233071'
mysql = MySQL(app)

msg = {0:"The username and password combination supplied does not match any accounts on record. Please try to login again or register if you are a new user.", 1:"Please login using the fields below."}

auth_user = -1

def q_user_auth(username, password):
    return '''SELECT userid FROM USERS where uname='''+"'" +username+"' and password=" + "'" + password + "'"

def q_reg_user(username, password):
    conn = mysql.connection
    cur = conn.cursor()
    id_max = 0
    cur.execute('''SELECT userid FROM USERS''')
    for id in cur.fetchall():
        if id[0] > id_max:
            id_max = int(id[0]) + 1
    return ['''INSERT INTO USERS ( USERID, UNAME, PASSWORD) VALUES''' + "(" +  "'" + str(id_max) + "'" + "," + "'" + username + "'" + "," + "'" + password + "'" + ")", id_max]

def q_get_users():
    conn = mysql.connection
    cur = conn.cursor()
    cmd = "SELECT userid, UNAME FROM USERS"
    cur.execute(cmd)
    return cur.fetchall()

def clean(result):
    List = list()
    for t in result:
        List.append(int(t[0]))
    List = ",".join(map(str,List))
    return List

def q_get_timeline():
    conn = mysql.connection
    cur = conn.cursor()
    cmd = "SELECT TID, MSG FROM TWEETS WHERE USERID IN (SELECT USERID FROM FOLLOWS WHERE FOLLOWER =" + str(auth_user) + " ) ORDER BY TSTAMP"
    cur.execute(cmd)
    return cur.fetchall()

def q_get_userid(uname):
    conn = mysql.connection
    cur = conn.cursor()
    cmd = "SELECT userid FROM USERS WHERE uname=" + "'" + uname + "'"
    cur.execute(cmd)
    return cur.fetchall()

def q_get_tweets(userid):
    conn = mysql.connection
    cur = conn.cursor()
    cmd = "SELECT * FROM TWEETS WHERE USERID=" + "'" + str(userid) + "'"
    print cmd
    cur.execute(cmd)
    return cur.fetchall()


@app.route('/user/<uname>', methods=['GET', 'POST'])
def user_page(uname):
    print clean(q_get_userid(uname))
    return render_template('userpage.html', uname = uname, tweets = q_get_tweets(clean(q_get_userid(uname))))

@app.route('/users', methods=['GET', 'POST'])
def userlist():
    return render_template('userlist.html', users = q_get_users())

@app.route('/timeline', methods=['GET', 'POST'])
def timeline():
    print auth_user
    tweets = q_get_timeline()
    print tweets
    return render_template('timeline.html', user = auth_user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        username =  request.form['usr']
        password = request.form['psw']
        print username
        print password
        string = q_user_auth(username, password)
        print string
        cur.execute(string)
        List = clean(cur.fetchall())
        # List = list()
        # for t in result:
        #     List.append(int(t[0]))
        # List = ",".join(map(str,List))
        print List
        global auth_user
        auth_user = List
        if len(List) != 0:
            return render_template('redir.html')
        else:
            return render_template('login.html', display = msg[0])

    return render_template('login.html', display = msg[1])

@app.route('/register', methods=['GET', 'POST'])
def register():
    conn = mysql.connection
    cur = conn.cursor()
    if request.method == 'POST':
        username =  request.form['usr']
        password = request.form['psw']
        print username
        print password
        query = q_reg_user(username, password)
        string = query[0]
        print string
        try:
            cur.execute(string)
            conn.commit()
            global auth_user
            auth_user = query[1]
            return render_template('redir.html')
        except mysql.connection.IntegrityError as err:
            print("Error: {}".format(err))
            return render_template('register.html', display = "That username is already taken. Please try again.")

    return render_template('register.html')

@app.route('/', methods=['GET', 'POST'])
def index():

    return render_template('index.html')

if __name__ == "__main__":
    app.run(use_reloader=True)
