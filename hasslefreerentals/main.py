import os
from flask import (
    Blueprint, flash, g, jsonify, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from hasslefreerentals.auth import login_required
from hasslefreerentals.db import get_db

bp = Blueprint('main', __name__)

# Configure global usertypes
USER_TYPES = ["Lessor", "Lessee"]

# Configure global equipment status
STATUS = ['Available', 'Unavailable']

# Configure global equipment categories
CAT =   {
    "Asphalt": ["Asphalt Paver", "Asphalt Scrapper"],
    "Compaction": ["Single Drum Smooth Wheeled Roller","Pneumatic Roller"],
    "Concrete and Masonry": ["Concrete Pump Truck", "Concrete Mixer Truck",],
    "Earthwork":["Chain Excavator", "Bull-Dozer", "Grader", "Loader", "Back Hoe"],
    "Trucks and Trailers":["Dump Truck", "Low-bed Truck"]
    }


@bp.route("/")
def index():
    return render_template("main/index.html", CAT = CAT)


@bp.route("/equipments")
@login_required
def equipments():
    # Equipments page will let users browse equipments on database
    return render_template("main/equipments.html", CAT = CAT)


@bp.route("/equipments_detail", methods = ['POST'])
@login_required
def equipments_detail():
    subcategory = request.form.get('subcategory')
    db = get_db()
    error = None
    
    if error == None:
        equipments = db.execute("SELECT * FROM equipment WHERE sub_category = ?", (subcategory,)).fetchall()
        if equipments == []:
            error = "No equipments found"
        flash(error)
        return render_template("main/equipments_detail.html", equipments=equipments, sub_category=subcategory, CAT=CAT )
    
    
@bp.route("/screturn")
def screturn():
    cat = request.args.get("cat")
    if cat:
        subcat = CAT[cat]       
    else:
        subcat = []
    return jsonify(subcat)


@bp.route('/eqregister', methods=['GET', 'POST'])
@login_required
def eqregister():
    if request.method == 'POST':
        db = get_db()
        owner_id = g.user['id']
        category= request.form["category"]
        sub_category = request.form["sub_category"]
        brand = request.form["brand"]
        model = request.form["model"]
        license_plate_no = request.form["license_plate_no"]
        fuel_type = request.form["fuel_type"]
        hp = request.form["hp"]
        year = request.form["year"]
        hourly_rate = request.form["hourly_rate"]
        advance = request.form["advance"]
        duration = request.form["duration"]
        location = request.form["location"]
        status = request.form["status"]
        # Get default image id
        def_img_id = db.execute('SELECT id FROM default_images WHERE name = ?', (sub_category,)).fetchone()[0]
        db.execute (
            "INSERT INTO equipment(owner_id, def_img_id, category, sub_category, brand, model, license_plate_no, fuel_type, hp, year, hourly_rate, advance, duration, location, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", 
            (owner_id, def_img_id, category, sub_category, brand, model, int(license_plate_no), fuel_type, int(hp), int(year), int(hourly_rate), int(advance), duration, location, status),
            )
        db.commit()
        return redirect (url_for('main.index'))
    return render_template('main/eqregister.html', CAT=CAT, STATUS=STATUS)

