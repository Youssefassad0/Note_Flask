from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required, current_user

from . import db
from .models import User

contrats = Blueprint("contrats", __name__)

@contrats.route("/search_contrat", methods=["GET", "POST"])
@login_required
def search_page():
    if request.method == "POST":
        numero_contrat = request.form.get("numero_contrat")
        
        if not numero_contrat:
            flash("Veuillez entrer un numéro de contrat valide.", "error")
            return redirect(url_for('search_page'))  # Redirect back to search page
        
        return render_template("contrats/update_contrat.html", nm=numero_contrat,user=current_user)

    return render_template("contrats/search.html",user=current_user)