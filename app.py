from flask import Flask,render_template, request
from flask_mysqldb import MySQL
app = Flask(__name__)
app.config['MYSQL_HOST'] = 'sql9.freemysqlhosting.net'
app.config['MYSQL_USER'] = 'sql9233071'
app.config['MYSQL_PASSWORD'] = '1uXgh92Fwi'
app.config['MYSQL_DB'] = 'sql9233071'
mysql = MySQL(app)

tables = {}
def findtables(substr):
    ans = {}
    for table in tables:
        if table.find(substr) > -1:
            ans[table] = tables[table]
    return ans

def find_attr(item):
    ans = {}
    for table in tables:
        if item in tables[table]:
            ans[table] = tables[table]
    return ans

def get_attr(name):
    return tables[field]

@app.route('/<item>', methods=['GET', 'POST'])
def attr_router(item):
    target_tables = find_attr(item)
    return render_template('data.html', target_tables=target_tables)

@app.route('/', methods=['GET', 'POST'])
def index():
    cur = mysql.connection.cursor()
    cur.execute('''SELECT table_name FROM information_schema.tables where table_type="base table"''')
    t_names = cur.fetchall()
    i = 0
    for name in t_names:
            str = "DESCRIBE" +' '+ name[0]
            cur.execute(str)
            t_vals = cur.fetchall()
            vals = []

            for j in range(len(t_vals)):
                vals.append(t_vals[j][0])
                ++j
            tables[name[0]] = vals
            ++i

    if request.method == 'POST':
        target_tables = findtables(request.form['target'])
        return render_template('data.html', target_tables=target_tables)

    return render_template('index.html')
if __name__ == "__main__":
    app.run(use_reloader=True)
