from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash
from . import db
from .models import User, HistoryLog
from datetime import datetime

users = Blueprint("users", __name__)


@users.route("/create_user", methods=["GET", "POST"])
@login_required
def create_user():
    print(f"Current user: {current_user} (Role: {getattr(current_user, 'role', None)})")

    if current_user.role != "2":  # Use integer comparison if role is an integer in DB
        flash(
            "Access denied: You do not have permission to create users.",
            category="error",
        )
        return redirect(url_for("views.home"))

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
        elif len(password) < 4:
            flash("Password must be greater than 6 characters.", category="error")
        elif not role:
            flash("Role must be selected.", category="error")
        elif User.query.filter_by(email=email).first():
            flash(
                "Email is already in use. Please use a different email.",
                category="error",
            )
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
            return redirect(url_for("users.create_user"))

    return render_template(
        "signup.html", user=current_user
    )  # Pass current_user to template


@users.route("/view_users", methods=["GET", "POST"])
@login_required
def view_users():
    if current_user.role == "2":
        users_list = User.query.all()  # Get all users
        return render_template(
            "view_users.html", user=current_user, users=users_list
        )  # Pass both current_user and users
    else:
        flash(
            "Access denied: You do not have permission to delete users.",
            category="error",
        )
        return redirect(url_for("views.home"))


@users.route("/delete/<int:user_id>", methods=["GET"])
@login_required
def delete_user(user_id):

    user_to_delete = User.query.get_or_404(user_id)
    if user_to_delete == current_user:
        flash("You cannot delete your own account.", category="error")
        return redirect(url_for("users.view_users"))
    # Delete the user
    db.session.delete(user_to_delete)
    try:
        db.session.commit()
        log_entry = HistoryLog(
            user_id=current_user.id,
            action="Delete user",
            details=f"Update Login to : {user_to_delete.login}  , name to : {user_to_delete.name} role to : {user_to_delete.role}",
            timestamp=datetime.now(),
        )
        db.session.add(log_entry)
        db.session.commit()
        flash("User deleted successfully!", category="success")
        return redirect(url_for("users.view_users"))
    except Exception as e:
        db.session.rollback()
        flash(f"An error occurred: {str(e)}", "error")
        return redirect(request.url)


@users.route("/update_user/<int:user_id>", methods=["GET", "POST"])
@login_required
def update_user(user_id):
    if current_user.role != "2":
        flash("You do not have permission to update users.", "error")
        return redirect(url_for("views.home"))

    user_to_update = User.query.get_or_404(user_id)

    if request.method == "POST":
        # Get data from the form
        login = request.form.get("login")
        name = request.form.get("name")
        password = request.form.get("password")
        role = request.form.get("role")

        # Validate inputs
        if not login or not name or not password or not role:
            flash("All fields are required.", "error")
            return redirect(request.url)

        # Update user fields
        user_to_update.login = login
        user_to_update.name = name
        user_to_update.password = generate_password_hash(
            password, method="pbkdf2:sha256"
        )
        user_to_update.role = role

        # Commit changes to the database
        try:
            db.session.commit()
            log_entry = HistoryLog(
                user_id=current_user.id,
                action="Updated user",
                details=f"Update Login to : {login}, name to : {name} role to : {role}",
                timestamp=datetime.now(),
            )
            db.session.add(log_entry)
            db.session.commit()
            flash("User updated successfully!", "success")
            return redirect(url_for("users.view_users")) 
        except Exception as e:
            db.session.rollback()
            flash(f"An error occurred: {str(e)}", "error")
            return redirect(request.url)

    return render_template("update_user.html", user=user_to_update)

@users.route("/history")
@login_required
def history():
    logs = db.session.query(HistoryLog, User).join(User, HistoryLog.user_id == User.id).all()

    for log, user in logs:
        print(f"{log.action} performed by {user.name} at {log.timestamp}")
