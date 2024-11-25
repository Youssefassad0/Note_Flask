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
    # Fetch the contract and vehicle details
    contrat = RA.query.filter_by(Number=nm_contrat).first()
    contrat_vehicule = RA_Vehicles.query.filter_by(RA=nm_contrat).first()

    if not contrat or not contrat_vehicule:
        flash("Contrat not found.", "error")
        return redirect(url_for("contrats.search_page"))

    # Capture the changes made
    changes = {}

    # Update contract fields and log changes
    for field in ["Close_Date", "Close_User", "Date_Out", "Date_In", "Return_Date", "Station_Out", "Station_In", "Return_Station", "Return_Place"]:
        old_value = getattr(contrat, field, None)
        new_value = request.form.get(field, None)
        if new_value and str(old_value) != new_value:
            changes[field] = {"old": old_value, "new": new_value}
            setattr(contrat, field, new_value)

    # Update vehicle fields and log changes
    for field in ["Plate_Number", "Kms_Out", "Kms_In"]:
        old_value = getattr(contrat_vehicule, field, None)
        new_value = request.form.get(field, None)
        if new_value and str(old_value) != new_value:
            changes[field] = {"old": old_value, "new": new_value}
            setattr(contrat_vehicule, field, new_value)

    # Commit the changes to the database
    db.session.commit()

    # Log the changes in the HistoryLog table
    if changes:
        log_entry = HistoryLog(
            user_id=current_user.id,  # Assuming Flask-Login is being used
            action="update",
            target_contrat_id=contrat.Number,
            details=json.dumps(changes)  # Store changes as a JSON string
        )
        db.session.add(log_entry)
        db.session.commit()

    flash("Modification Avec Succès.", "success")
    return redirect(url_for("contrats.search_page"))
