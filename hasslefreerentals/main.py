import os
import io
from flask import (
    Blueprint, flash, g, jsonify, redirect, render_template, request, session, send_file, url_for
)
from werkzeug.exceptions import abort

from hasslefreerentals.auth import login_required
from hasslefreerentals.db import get_db

bp = Blueprint('main', __name__)

# Configure global equipment status
STATUS = ['Available', 'Unavailable']

# Configure global fuel options
FUEL_TYPE = ['Diesel', 'Petrol', 'Electric']

# Configure global duration preferences
DUR = ['Long Term', 'Short Term']

# Configure global equipment categories
CAT =   {
    "Asphalt": ["Asphalt Paver", "Asphalt Scrapper"],
    "Compaction": ["Single Drum Smooth Wheeled Roller","Pneumatic Roller"],
    "Concrete and Masonry": ["Concrete Pump Truck", "Concrete Mixer Truck",],
    "Earthwork":["Chain Excavator", "Bull-Dozer", "Grader", "Loader", "Back Hoe"],
    "Trucks and Trailers":["Dump Truck", "Low-bed Truck"]
    }

POP_SCS = ['Chain Excavator', 'Dump Truck', 'Low-bed Truck', 'Back Hoe', 'Concrete Pump Truck', 'Concrete Mixer Truck']
ALL_SCS = ['Pneumatic Roller','Chain Excavator','Concrete Pump Truck','Asphalt Scrapper','Loader','Single Drum Smooth Wheeled Roller','Grader','Asphalt Paver','Low-bed Truck','Concrete Mixer Truck','Bull-Dozer','Dump Truck','Back Hoe']


@bp.route('/image/<int:image_id>')
def get_image(image_id):
    db = get_db()
    # Retrieve the image data based on the provided image ID
    image_data = db.execute('SELECT image_data FROM default_images WHERE id = ?', (image_id,)).fetchone()[0]

    # Return the image data with the appropriate content type
    return send_file(io.BytesIO(image_data), mimetype='image/jpeg')


def makesubcat_defaultimgid_dict(subcatlist):
    db = get_db()
    subcat_imgid_dict = {}
    for subcat in subcatlist:
        subcat_imgid_dict[subcat] = db.execute('SELECT id FROM default_images WHERE name = ?', (subcat,)).fetchone()[0]
    return subcat_imgid_dict


def get_equipment(id, check_owner=True):
    db = get_db()
    equipment = db.execute('SELECT * FROM equipment WHERE id = ?',(id,)).fetchone()

    if equipment is None:
        abort(404, f"Equipment id {id} doesn't exist.")

    if check_owner and equipment['owner_id'] != g.user['id']:
        abort(403)

    return equipment


@bp.route("/")
def index():
    img_dict = makesubcat_defaultimgid_dict(POP_SCS)    
    return render_template("main/index.html", CAT=CAT, popularsubcats=POP_SCS, img_dict=img_dict)
    
@bp.route("/equipments")
@login_required
def equipments():
    return redirect(url_for('main.browse_equipments'))
    
        

@bp.route("/browse_equipments")
@login_required
def browse_equipments():
    img_dict = makesubcat_defaultimgid_dict(POP_SCS)
    return render_template("main/equipments.html", CAT=CAT, popularsubcats=POP_SCS, img_dict=img_dict)

@bp.route("/equipments_detail", methods = ['POST'])
@login_required
def equipments_detail():
    subcategory = request.form.get('sub_category')
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

@bp.route("/eqregister")
@login_required
def eqregister():
    if session.get('user_type') == 'Lessor':
        return redirect(url_for('main.register_requipments'))
    else:
        error = 'Only "Lessor" user types can register equipment. Please login using a "Lessor" account'
        flash(error)
        return redirect(url_for('main.browse_equipments'))


@bp.route('/register_requipments', methods=['GET', 'POST'])
@login_required
def register_requipments():
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
    return render_template('main/eqregister.html', CAT=CAT, STATUS=STATUS, FUEL_TYPE=FUEL_TYPE, DUR=DUR )


@bp.route('/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update(id):
    equipment = get_equipment(id)
    print('----------------------------------')
    print('Inside update')
    
    if request.method == 'POST':
        category= request.form["category"]
        print('----------------------------------')
        print(category)
        sub_category = request.form["sub_category"]
        print(sub_category)
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
        error = None
        
        #Insert form validations here
        if not category:
            error = 'Category is required.'
        if not sub_category:
            error = 'Subcategory is required.'
        
        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                "UPDATE equipment SET category = ?, sub_category = ?, brand = ?, model = ?, license_plate_no = ?, fuel_type = ?, hp = ?, year = ?, hourly_rate = ?, advance = ?, duration = ?, location = ?, status = ? WHERE id = ?",
                (category, sub_category, brand, model, int(license_plate_no), fuel_type, int(hp), int(year), int(hourly_rate), int(advance), duration, location, status, id),
            )
            db.commit()
            return redirect(url_for('main.dashboard'))
            
    return render_template('main/update.html', equipment=equipment,  CAT=CAT, STATUS=STATUS, FUEL_TYPE=FUEL_TYPE, DUR=DUR)


@bp.route('/dashboard')
@login_required
def dashboard():
    db = get_db()
    # Get all the user equipment
    user_equipments = db.execute(
        "SELECT * FROM equipment WHERE owner_id = ?", (g.user['id'],)).fetchall()
    img_dict = makesubcat_defaultimgid_dict(ALL_SCS)
    return render_template('main/dashboard.html', user_equipments=user_equipments, img_dict=img_dict)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_equipment(id)
    db = get_db()
    db.execute('DELETE FROM equipment WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('main.dashboard'))


@bp.route("/booking")
def booking():
    return render_template("main/booking.html")