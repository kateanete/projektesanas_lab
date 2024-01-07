import csv
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))


class Food(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product = db.Column(db.String(150))
    dish_time = db.Column(db.String(150))
    allergens = db.Column(db.String(150))
    allergies = db.Column(db.String(150))
    kcal_per_100gr = db.Column(db.Float)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user = db.relationship("User", backref=db.backref("foods", lazy=True))

    @staticmethod
    def import_food_data(file_path):
        with open(file_path, "r") as file:
            reader = csv.reader(file)
            next(reader)  # Skip header row
            for row in reader:
                product, dish_time, allergens, allergies, kcal_per_100gr = row
                food = Food(
                    product=product,
                    dish_time=dish_time,
                    allergens=allergens,
                    allergies=allergies,
                    kcal_per_100gr=float(kcal_per_100gr),
                )
                db.session.add(food)
        db.session.commit()


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship("Note")
