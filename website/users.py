from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash
from . import db
from .models import User

users = Blueprint('users', __name__)

@users.route('/create_user', methods=["GET", "POST"])
@login_required
def create_user():
    print(f"Current user: {current_user} (Role: {getattr(current_user, 'role', None)})")

    # Skip role check for now and allow access to test
    # if current_user.role != 2:  # Use integer comparison if role is an integer in DB
    #     flash("Access denied: You do not have permission to create users.", category="error")
    #     return redirect(url_for("views.home"))

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
        elif len(password) <4:
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
                password=generate_password_hash(password, method="pbkdf2:sha256"),
                role=role,
            )
            db.session.add(new_user)
            db.session.commit()

            flash("User created successfully!", category="success")
            return redirect(url_for("views.home"))

    return render_template("signup.html", user=current_user)  # Pass current_user to template


@users.route('/view', methods=["GET"])
@login_required
def view_users():
   
    if current_user.role != "2":
        flash("Access denied: You do not have permission to view users.", category="error")
        return redirect(url_for("views.home"))

    users_list = User.query.all()  # Retrieve all users from the database
    return render_template("view_users.html",user=current_user, users=users_list)


@users.route('/delete/<int:user_id>', methods=["GET"])
@login_required
def delete_user(user_id):
    # Only allow access if the user has role "2"
    if current_user.role != "2":
        flash("Access denied: You do not have permission to delete users.", category="error")
        return redirect(url_for("views.home"))

    # Fetch the user to delete
    user_to_delete = User.query.get_or_404(user_id)

    # Ensure you can't delete yourself
    if user_to_delete == current_user:
        flash("You cannot delete your own account.", category="error")
        return redirect(url_for("users.view_users"))

    # Delete the user
    db.session.delete(user_to_delete)
    db.session.commit()

    flash("User deleted successfully!", category="success")
    return redirect(url_for("users.view_users"))
