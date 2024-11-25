from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required, current_user

from . import db
from .models import RA, RA_Vehicles,HistoryLog

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
    # Fetch the contract to be updated
    contrat = RA.query.filter_by(Number=nm_contrat).first()
    contrat_vehicule = RA_Vehicles.query.filter_by(RA=nm_contrat).first()

    if not contrat:
        flash("Contract not found.", "error")
        return redirect(url_for("contrats.search_page"))

    # Update the contract fields
    contrat.Close_Date = request.form.get("Close_Date") or contrat.Close_Date
    contrat.Close_User = request.form.get("Close_User") or contrat.Close_User
    contrat.Date_Out = request.form.get("Date_Out") or contrat.Date_Out
    contrat.Date_In = request.form.get("Date_In") or contrat.Date_In
    contrat.Return_Date = request.form.get("Return_Date") or contrat.Return_Date
    contrat.Station_Out = request.form.get("Station_Out") or contrat.Station_Out
    contrat.Station_In = request.form.get("Station_In") or contrat.Station_In
    contrat.Return_Station = request.form.get("Return_Station") or contrat.Return_Station
    # Update the contract_vehicles fields
    contrat_vehicule.Plate_Number= request.form.get("Plate_Number") or contrat.Plate_Number
    contrat_vehicule.Kms_Out= request.form.get("Kms_Out") or contrat.Kms_Out
    contrat_vehicule.Kms_In= request.form.get("Kms_In") or contrat.Kms_In
    # Commit changes to the database
    db.session.commit()


    log_entry = HistoryLog(
        user_id=current_user.id,
        action="update",
        details="Updated contract fields."
    )
    db.session.add(log_entry)
    db.session.commit()

    flash("Modification Avec Succès.", "success")
    return redirect(url_for("contrats.search_page"))
