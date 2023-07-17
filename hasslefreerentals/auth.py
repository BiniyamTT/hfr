import functools
import requests

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
    )
from werkzeug.security import check_password_hash, generate_password_hash

from hasslefreerentals.db import get_db

# Configure global usertypes
USER_TYPES = ["Lessor", "Lessee"]

bp = Blueprint('auth', __name__, url_prefix='/auth')

apisecret = "1ccdc141f237b2c18dfb44dc7716095c2f1ada70"

def verifyotp(otp):
    # Verify OTP using hahu.io API  
    r = requests.get(url = "https://hahu.io/api/get/otp", params = {
        "secret": apisecret,
        "otp": otp
    })
    # Get status code from verification and return it
    return(r.json()['status'])
    

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    
    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()


@bp.after_app_request
def clear_response_cache(response):
    # Ensure responses aren't cached
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = 0
    return response  


@bp.route('/sendotp', methods=['POST'])
def sendotp():
    if request.method == 'POST':
        data = request.form.get('data')
        message = {
            "secret": apisecret,
            "type": "sms",
            "mode": "devices",
            "device": "00000000-0000-0000-0aa2-9d90a03739af",
            "sim": 2,
            "phone": data,
            "message": "Your OTP is {{otp}}"}
        r = requests.post(url = "https://hahu.io/api/send/otp", params = message)
        return (r.json)

@bp.route('/register', methods = ['GET', 'POST'])
def register():
    # Register a new user.
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        phoneno = request.form['phoneno']
        verificationcode = request.form['otp']
        usertype = request.form['usertype']
        password = request.form['password']
        confirmation = request.form['confirmation']
        db = get_db()
        error = None
        
        if not firstname:
            error = 'First name is required.'
        elif not lastname:
            error = 'Last name is required.'
        elif not phoneno:
            error = 'Phone number is required.'
        elif not usertype:
            error = 'User type is required.'
        elif not password:
            error = 'Password is required.'
        elif password != confirmation:
            error = 'Passwords do not match.'
        elif verifyotp(verificationcode) != 200:
            error = 'OTP either invalid or expired, try again.'
        
        if error is None:
            try:
                db.execute(
                    "INSERT INTO user (firstname, lastname, email, phoneno, usertype, hash) VALUES (?, ?, ?, ?, ?, ?)",
                    (firstname, lastname, email, phoneno, usertype, generate_password_hash(password)),
                )
                db.commit()
                flash("User registered successfully. Log in to continue.")
            except db.IntegrityError:
                error = f"The phone number {phoneno} is already registered. Log in to continue."
            else:
                return redirect(url_for("auth.login"))
        
        flash(error)
        
    return render_template('auth/register.html', usertypes = USER_TYPES)


@bp.route('/login', methods = ['GET', 'POST'])
def login():
    # Log in a registered user.
    if request.method == "POST":
        phoneno = request.form['phoneno']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE phoneno = ?', (phoneno,)
        ).fetchone()
        
        if user is None:
            error = 'Incorrect Phone number.'
        elif not check_password_hash(user['hash'], password):
            error = 'Incorrect password.'
        
        if error is None:
            session.clear()
            session['user_id'] = user['id']
            session['user_type'] = user['usertype']
            g.user_type = user['usertype']
            return redirect(url_for('index'))
        
        flash(error)

    return render_template('auth/login.html')


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))
