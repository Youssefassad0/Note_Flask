from flask import Blueprint, render_template, request, flash

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("login")
        password = request.form.get("password")
    return render_template("login.html")


@auth.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form.get("login")
        name = request.form.get("name")
        role = request.form.get("role")
        password = request.form.get("password")
        if len(email) <= 4:
            flash("Login Must be greater than 4 caratcters .", category="error")
        elif len(name) <= 2:
            flash("Name Must be greater than 2 caratcters .", category="error")
        elif len(password) <= 6:
            flash("Password Must be greater than 6 caratcters .", category="error")
        elif role == "":
            flash("Role Must be Selected .", category="error")
        else:
            flash("You created the user correctly !", category="success")
    return render_template("signup.html")


@auth.route("/Logout")
def logout():
    return "logout"
