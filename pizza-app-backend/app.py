from flask import Flask, render_template, request, jsonify, json, make_response
from flask_mysqldb import MySQL

app = Flask(__name__)
# CORS(app)

app.config['MYSQL_HOST'] = 'remotemysql.com'
app.config['MYSQL_USER'] = ''
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = ''

mysql = MySQL(app)

def corsapp_route(path, origin=('127.0.0.1',), **options):
    """
    Flask app alias with cors
    :return:
    """

    def inner(func):
        def wrapper(*args, **kwargs):
            if request.method == 'OPTIONS':
                response = make_response()
                response.headers.add("Access-Control-Allow-Origin", ', '.join(origin))
                response.headers.add('Access-Control-Allow-Headers', ', '.join(origin))
                response.headers.add('Access-Control-Allow-Methods', ', '.join(origin))
                return response
            else:
                result = func(*args, **kwargs)
            if 'Access-Control-Allow-Origin' not in result.headers:
                result.headers.add("Access-Control-Allow-Origin", ', '.join(origin))
            return result

        wrapper.__name__ = func.__name__

        if 'methods' in options:
            if 'OPTIONS' in options['methods']:
                return app.route(path, **options)(wrapper)
            else:
                options['methods'].append('OPTIONS')
                return app.route(path, **options)(wrapper)

        return wrapper

    return inner


@corsapp_route("/", origin=['*'])
def main():
    return "Welcome!"


@corsapp_route("/add_entry", methods=['POST'], origin=['*'])
def add_entry():
    if request.method == "POST":
        number = request.form['number']
        address = request.form['address']
        order = request.form['order']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO MyUsers(num,addr,ord) VALUES (%s,%s,%s)", (number,address,order))
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


@corsapp_route("/get_entry", methods=['GET'], origin=['*'])
def get_entry():
    if request.method == "GET":
        number = request.args.get('address')

        cur = mysql.connection.cursor()
        cur.execute("SELECT * from MyUsers where num={num} ;".format(num=number))
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


@corsapp_route("/chiefRecommendations/pizza.json", methods=['GET'], origin=['*'])
def return_json_recs():
    if request.method == "GET":
        resp = [
                {
                "description": "Delicate pizza with cream sauce, tomatoes, mozzarella, parmesan, hunting sausages, arugula, paprika and oregano.",
                "img": "/img/menu/pizza/super-cheese.jpg",
                "numberOfPieces": 8,
                "price": 107,
                "slug": "super-cheese",
                "title": "Super Cheese"
                },
                {
                "description": "Flavored pizza with baked chicken, tomatoes, ham, mozzarella cheese, corn, olives, tomato sauce, white sesame seeds and oregano.",
                "img": "/img/menu/pizza/mexicano.jpg",
                "numberOfPieces": 8,
                "price": 97,
                "slug": "mexicano",
                "title": "Mexicano"
                },
                {
                "description": "Pizza, combining 4 different bright flavors. The composition of the filling: chicken, corn, pineapple, squid, mussels, snow crab, bacon, mushrooms, onions, tomatoes, pork and mozare cheese ...",
                "img": "/img/menu/pizza/four-seasons.jpg",
                "numberOfPieces": 8,
                "price": 116,
                "slug": "four-seasons",
                "title": "4 Seasons"
                },
                {
                "description": "Meat pizza with tomato sauce, smoked chicken, hunting sausages, salami, tomatoes, parmesan, ham and mozzarella, seasoned with Italian herbs.",
                "img": "/img/menu/pizza/four-meats.jpg",
                "numberOfPieces": 8,
                "price": 123,
                "slug": "four-meats",
                "title": "4 Meats"
                }
            ]
        resp = jsonify(resp)
        resp.status_code = 200
        return resp
    
    resp = {"File": "Not Present"}
    resp = jsonify(resp)
    resp.status_code = 400
    return resp


@corsapp_route("/dishes/pizza.json", methods=['GET'],  origin=['*'])
def return_json_rec1():
    if request.method == "GET":
        resp = {
            "four-cheese": {
                "description": "Pizza with creamy sauce and four types of cheese: mozzarella, Dutch, parmesan, dorblu and cherry tomatoes, seasoned with Italian herbs.",
                "img": "/img/menu/pizza/four-cheese.jpg",
                "ingredients": [
                    "Oregano",
                    "Creamy garlic sauce",
                    "Mozzarella",
                    "Parmesan Cheese",
                    "Dor Blue Cheese",
                    "Cherry tomatoes",
                    "Hard cheese"
                    ],
                    "numberOfPieces": 8,
                    "nutrition": {
                    "calories": 269,
                    "fats": 12,
                    "glicides": 30,
                    "protein": 11
                    },
                "price": 117,
                "slug": "four-cheese",
                "title": "4 сыра"
            },
            "four-meats": {
                "description": "Meat pizza with tomato sauce, smoked chicken, hunting sausages, salami, tomatoes, parmesan, ham and mozzarella, seasoned with Italian herbs.",
                "img": "/img/menu/pizza/four-meats.jpg",
                "ingredients": [
                "Oregano",
                "Tomatoes",
                "Mozzarella",
                "Tomato sauce",
                "Salami",
                "Ham",
                "Parmesan Cheese",
                "Hunting sausages",
                "Smoked chicken"
                ],
                "numberOfPieces": 8,
                "nutrition": {
                "calories": 380,
                "fats": 18,
                "glicides": 42,
                "protein": 15
                },
                "price": 123,
                "slug": "four-meats",
                "title": "4 мяса"
            },
            "four-seasons": {
                "description": "Pizza, combining 4 different bright flavors. The composition of the filling: chicken, corn, pineapple, squid, mussels, snow crab, bacon, mushrooms, onions, tomatoes, pork and mozare cheese ...",
                "img": "/img/menu/pizza/four-seasons.jpg",
                "ingredients": [
                "Mozzarella",
                "Tomatoes",
                "Oregano",
                "Parmesan Cheese",
                "Hunting sausages",
                "Arugula",
                "Cream sauce"
                ],
                "numberOfPieces": 8,
                "nutrition": {
                "calories": 380,
                "fats": 18,
                "glicides": 42,
                "protein": 15
                },
                "price": 116,
                "slug": "four-seasons",
                "title": "4 Seasons"
            },
            "mexicano": {
                "description": "Flavored pizza with baked chicken, tomatoes, ham, mozzarella cheese, corn, olives, tomato sauce, white sesame seeds and oregano.",
                "img": "/img/menu/pizza/mexicano.jpg",
                "ingredients": [
                "Mozzarella",
                "Tomatoes",
                "Oregano",
                "Parmesan Cheese",
                "Hunting sausages",
                "Arugula",
                "Cream sauce"
                ],
                "numberOfPieces": 8,
                "nutrition": {
                "calories": 350,
                "fats": 15,
                "glicides": 45,
                "protein": 19
                },
                "price": 97,
                "slug": "mexicano",
                "title": "Mexicano"
            },
            "pepperoni": {
                "description": "Spicy pizza with tomato sauce, cherry tomatoes, pepperoni, parmesan, tomatoes and mozzarella seasoned with Italian herbs.",
                "img": "/img/menu/pizza/pepperoni.jpg",
                "ingredients": [
                "Mozzarella",
                "Tomatoes",
                "Oregano",
                "Parmesan Cheese",
                "Hunting sausages",
                "Arugula",
                "Cream sauce"
                ],
                "numberOfPieces": 8,
                "nutrition": {
                "calories": 290,
                "fats": 16,
                "glicides": 38,
                "protein": 14
                },
                "price": 127,
                "slug": "pepperoni",
                "title": "Pepperoni"
            },
            "spicy-meat": {
                "description": "Spicy pizza with tomato sauce, chili pepper, ground beef, tomatoes, pepperoni, bacon and mozzarella",
                "img": "/img/menu/pizza/spicy-meat.jpg",
                "ingredients": [
                "Mozzarella",
                "Tomatoes",
                "Oregano",
                "Parmesan Cheese",
                "Hunting sausages",
                "Arugula",
                "Cream sauce"
                ],
                "numberOfPieces": 8,
                "nutrition": {
                "calories": 300,
                "fats": 17,
                "glicides": 35,
                "protein": 15
                },
                "price": 112,
                "slug": "spicy-meat",
                "title": "Spicy Meat"
            },
            "super-cheese": {
                "description": "Delicate pizza with cream sauce, tomatoes, mozzarella, parmesan, hunting sausages, arugula, paprika and oregano.",
                "img": "/img/menu/pizza/super-cheese.jpg",
                "ingredients": [
                "Mozzarella",
                "Tomatoes",
                "Oregano",
                "Parmesan Cheese",
                "Hunting sausages",
                "Arugula",
                "Cream sauce"
                ],
                "numberOfPieces": 8,
                "nutrition": {
                "calories": 425,
                "fats": 12,
                "glicides": 35,
                "protein": 25
                },
                "price": 107,
                "slug": "super-cheese",
                "title": "Super Cheese"
            },
            "super-meat": {
                "description": "Meat pizza with tomato sauce, tender chicken, bacon, jerky, salami, pork, ham and mozzarella, seasoned with Italian herbs.",
                "img": "/img/menu/pizza/super-meat.jpg",
                "ingredients": [
                "Oregano",
                "Bacon",
                "Mozzarella",
                "Tomato sauce",
                "Chicken fillet",
                "Cured meat",
                "Salami",
                "Ham",
                "Pork"
                ],
                "numberOfPieces": 8,
                "nutrition": {
                "calories": 282,
                "fats": 15,
                "glicides": 21,
                "protein": 15
                },
                "price": 126,
                "slug": "super-meat",
                "title": "Super MEAT"
            }
            }
        resp = jsonify(resp)
        resp.status_code = 200
        return resp
    
    resp = {"File": "Not Present"}
    resp = jsonify(resp)
    resp.status_code = 400
    return resp
    



if __name__ == "__main__":
    app.run()
