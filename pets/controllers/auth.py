from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import check_password_hash

from pets.models.manager import Manager

auth = Blueprint('auth', __name__)


@auth.route('/login')
def login():
    return render_template('login.html', next=request.args.get("next", "/"))


@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    manager = Manager.query.filter_by(email=email.lower()).first()

    # check if user actually exists
    # take the user supplied password, hash it, and compare it to the hashed password in database
    if not manager or not check_password_hash(manager.password, password) or not manager.is_employed:
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login'))  # if user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    login_user(manager, remember=remember)
    return redirect(request.args.get("next", "/"))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
