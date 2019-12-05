from flask import Flask, render_template, request, jsonify
from flask_mysqldb import MySQL

app = Flask(__name__)


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'MyDB'

mysql = MySQL(app)

@app.route("/")
def main():
    return "Welcome!"

@app.route("/add_entry", methods=['POST'])
def add_entry():
    if request.method == "POST":
        number = request.form['number']
        address = request.form['address']
        order = request.form['order']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO MyUsers(number,address,order) VALUES (%s,%s,%s)", (number,address,order))
        mysql.connection.commit()
        cur.close()

        resp = {"Database": "Updated"}
        resp = jsonify(resp)
        resp.status_code = 200
        return resp
    
    resp = {"Database": "Not Updated"}
    resp = jsonify(resp)
    resp.status_code = 400
    return resp

@app.route("/get_entry", methods=['GET'])
def get_entry():
    if request.method == "GET":
        number = request.args.get('address')

        cur = mysql.connection.cursor()
        cur.execute("SELECT * from MyUsers where number=%s", (number))
        mysql.connection.commit()
        cur.close()

        resp = {"Database": cur.fetchall()}
        resp = jsonify(resp)
        resp.status_code = 200
        return resp
    
    resp = {"Database": "Not Present"}
    resp = jsonify(resp)
    resp.status_code = 400
    return resp




if __name__ == "__main__":
    app.run()