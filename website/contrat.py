from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required, current_user

from . import db
from .models import RA, RA_Vehicles

contrats = Blueprint("contrats", __name__)


@contrats.route("/search_contrat", methods=["GET", "POST"])
@login_required
def search_page():
    if request.method == "POST":
        numero_contrat = request.form.get("numero_contrat")

        if numero_contrat:
            contrat = RA.query.filter_by(Number=numero_contrat).first()
            contrat_vehicule = RA_Vehicles.query.filter_by(RA=numero_contrat).first()
            return render_template(
                "contrats/update_contrat.html",
                contrat=contrat,
                contrat_vehicule=contrat_vehicule,
                user=current_user,
            )
        else:
            flash("Veuillez entrer un numéro de contrat valide.", "error")
            return redirect(url_for("contrats.search_page"))

    return render_template("contrats/search.html", user=current_user)

@contrats.route("/update_contrat/<int:nm_contrat>", methods=["POST"])
@login_required
def update_contrat(nm_contrat):
    print (nm_contrat)
    flash("Modification Avec Succes .", "success")

    return redirect(url_for("contrats.search_page"))
    # contrat = RA.query.filter_by(Number=nm_contrat).first()
    # contrat_vehicule = RA_Vehicles.query.filter_by(RA=nm_contrat).first()
