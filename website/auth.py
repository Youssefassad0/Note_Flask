from flask import Blueprint, render_template, request, flash, url_for, redirect
from .models import User
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user , login_required , current_user , logout_user
auth = Blueprint("auth", __name__)

@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("login")
        password = request.form.get("password")

        # Check if the user exists
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash("Login successful!", category="success")
                login_user(user)
                # Redirect to the home page or dashboard
                return redirect(url_for("views.home"))
            else:
                flash("Incorrect password. Please try again.", category="error")
        else:
            flash("Email not found. Please sign up first.", category="error")
    
    return render_template("login.html")

@auth.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form.get("login")
        name = request.form.get("name")
        role = request.form.get("role")
        password = request.form.get("password")

        # Validate inputs
        if len(email) <= 4:
            flash("Email must be greater than 4 characters.", category="error")
        elif len(name) <= 2:
            flash("Name must be greater than 2 characters.", category="error")
        elif len(password) <= 6:
            flash("Password must be greater than 6 characters.", category="error")
        elif not role:
            flash("Role must be selected.", category="error")
        elif User.query.filter_by(email=email).first():
            flash("Email is already in use. Please use a different email.", category="error")
        else:
            # Create a new user
            new_user = User(
                email=email,
                name=name,
                password=generate_password_hash(password,  method='pbkdf2:sha256'),
                role=role
            )
            db.session.add(new_user)
            db.session.commit()
            flash("User created successfully!", category="success")
            return redirect(url_for("views.home"))

    return render_template("signup.html")

@auth.route("/logout")
def logout():
    # Clear user session or implement Flask-Login's logout_user()
    flash("You have been logged out.", category="info")
    return redirect(url_for("auth.login"))
