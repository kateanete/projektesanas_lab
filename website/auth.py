from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from flask_bcrypt import Bcrypt  # Import Bcrypt
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint("auth", __name__)
bcrypt = Bcrypt()  # Create a Bcrypt instance


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()
        if user:
            if bcrypt.check_password_hash(
                user.password, password
            ):  # Use Bcrypt for checking password
                flash("Logged in successfully!", category="success")
                login_user(user, remember=True)
                return redirect(url_for("views.home"))
            else:
                flash("Incorrect password, try again.", category="error")
        else:
            flash("Email does not exist.", category="error")

    return render_template("login.html", user=current_user)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
    
@auth.route('/edienkarte')
def edienkarte():
    return render_template("edienkarte.html", boolean=False)

@auth.route('/ievade',  methods=['GET', 'POST'])
def ievade():
    if request.method == 'POST':
        garums = request.form.get('garums')
        svars = request.form.get('svars')
        kalorijas = request.form.get('kalorijas')
        
        if garums is '':
            flash('Ievadiet garumu', category='error')
        elif svars is '':
            flash('Ievadiet svaru', category='error')
        elif kalorijas is '':
            flash('Ievadiet kaloriju daudzumu', category='error')
        else:
            flash ('Izmaiņas saglabātas, varat izveidot ēdienkarti.', category='success')

    return render_template("ievade.html")

@auth.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        email = request.form.get("email")
        first_name = request.form.get("firstName")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        height = request.form.get("height")
        weight = request.form.get("weight")
        calories = request.form.get("calories")

        user = User.query.filter_by(email=email).first()
        if user:
            flash("Email already exists.", category="error")
        elif len(email) < 4:
            flash("Email must be greater than 3 characters.", category="error")
        elif len(first_name) < 2:
            flash("First name must be greater than 1 character.", category="error")
        elif password1 != password2:
            flash("Passwords don't match.", category="error")
        elif len(password1) < 7:
            flash("Password must be at least 7 characters.", category="error")
        elif height is "":
            flash("Input correct height", category="error")
        elif weight is "":
            flash("Input correct weight", category="error")
        elif calories is "":
            flash("Input correct calorie amount", category="error")
        else:
            hashed_password = bcrypt.generate_password_hash(password1).decode(
                "utf-8"
            )  # Use Bcrypt for password hashing
            new_user = User(
                email=email,
                first_name=first_name,
                password=hashed_password,
                height=height,
                weight=weight,
                calories=calories,
            )
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash("Account created!", category="success")
            return redirect(url_for("views.home"))

    return render_template("sign_up.html", user=current_user)
