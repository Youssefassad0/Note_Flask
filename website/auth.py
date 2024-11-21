from flask import Blueprint, render_template, request, flash, url_for, redirect
from .models import User
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, current_user, logout_user

auth = Blueprint("auth", __name__)

@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("login")
        password = request.form.get("password")

        # Check if the user exists in the database
        user = User.query.filter_by(email=email).first()
        
        # If user exists and the password is correct
        if user and check_password_hash(user.password, password):
            flash("Login successful!", category="success")
            login_user(user, remember=True)  # Log in the user and remember them for next session
            return redirect(url_for("views.home"))  # Redirect to home after successful login

        # If user does not exist or the password is incorrect
        if not user:
            flash("Email not found. Please sign up first.", category="error")
        else:
            flash("Incorrect password. Please try again.", category="error")
    
    return render_template("login.html", user=current_user)  # Pass current_user to template


@auth.route("/logout")
@login_required
def logout():
    logout_user()  # Logs out the current user
    flash("You have been logged out.", category="info")  # Display a logout message
    return redirect(url_for("auth.login"))  # Redirect to login page after logout
