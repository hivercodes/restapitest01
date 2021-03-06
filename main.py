from flask import Flask, jsonify, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import random

app = Flask(__name__)

##Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


##Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)


@app.route("/")
def home():
    return render_template("index.html")



@app.route("/random")
def get_random_cafe():
    #choses a random databsae row.
    all_cafes = db.session.query(Cafe).all()
    cafe = random.choice(all_cafes)
    return jsonify(name=cafe.name,
        map_url=cafe.map_url,
        img_url=cafe.img_url,
        location=cafe.location,
        seats=cafe.seats,
        has_toilet=cafe.has_toilet,
        has_wifi=cafe.has_wifi,
        has_sockets=cafe.has_sockets,
        can_take_calls=cafe.can_take_calls,
        coffee_price=cafe.coffee_price)

@app.route("/all")
def all_cafes():
    #fetches all the items from the database
    all_cafes = db.session.query(Cafe).all()
    cafe_list = []
    for cafe in all_cafes:
        cafe_dict = {
        "name":cafe.name,
        "map_url":cafe.map_url,
        "img_url":cafe.img_url,
        "location":cafe.location,
        "seats":cafe.seats,
        "has_toilet":cafe.has_toilet,
        "has_wifi":cafe.has_wifi,
        "has_sockets":cafe.has_sockets,
        "can_take_calls":cafe.can_take_calls,
        "coffee_price":cafe.coffee_price}
        cafe_list.append(cafe_dict)

    return jsonify(cafe_list)


@app.route("/search")
def search():
    #search for the location via call
    place = request.args.get("loc")
    cafe = db.session.query(Cafe).filter_by(location=place).first()
    print(cafe)
    if cafe:
        return jsonify(name=cafe.name,
            map_url=cafe.map_url,
            img_url=cafe.img_url,
            location=cafe.location,
            seats=cafe.seats,
            has_toilet=cafe.has_toilet,
            has_wifi=cafe.has_wifi,
            has_sockets=cafe.has_sockets,
            can_take_calls=cafe.can_take_calls,
            coffee_price=cafe.coffee_price)
    else:
        return jsonify(error={"Not found": "No cafe found"})



@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        #makes a new cafe objecxt to add to the database."
        new_cafe = Cafe(name=request.form["name"],
        map_url=request.form["map_url"],
        img_url=request.form["img_url"],
        location=request.form["location"],
        seats=request.form["seats"],
        has_toilet=bool(request.form["has_toilet"]),
        has_wifi=bool(request.form["has_wifi"]),
        has_sockets=bool(request.form["has_sockets"]),
        can_take_calls=bool(request.form["can_take_calls"]),
        coffee_price=request.form["coffee_price"])
        db.session.add(new_cafe)
        db.session.commit()
        return jsonify(response={"Success": "Cafe added to database"})
    return render_template("index.html")

## HTTP GET - Read Record

## HTTP POST - Create Record

## HTTP PUT/PATCH - Update Record

## HTTP DELETE - Delete Record


if __name__ == '__main__':
    app.run(debug=True)
