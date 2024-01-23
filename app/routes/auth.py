from flask import render_template, session, redirect, flash, url_for, Blueprint
from app.forms import SignupForm, SigninForm
import bcrypt
from app.models import Users, db
import json

with open('config.json', 'r') as c:
    parameters = json.load(c)["parameters"]

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/signup", methods=['GET', 'POST'])
def sign_up():
    form = SignupForm()
    if form.validate_on_submit():
        user_name = form.user_name.data
        user_email = form.user_email.data
        password = form.password.data

        existing_user = Users.query.filter_by(user_email=user_email).first()

        if existing_user:
            flash("User with this Email already exists. Please use a different email.", 'warning')
            return redirect(url_for('auth.sign_up'))
        else:
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            entry = Users(user_name=user_name, user_email=user_email, password=hashed_password)
            db.session.add(entry)
            db.session.commit()
            flash("Sign up successful.")

        return redirect(url_for('auth.signin'))

    return render_template('sign-up.html', form=form, parameters=parameters)


@bp.route('/signin', methods=['GET', 'POST'])
def signin():
    form = SigninForm()
    if form.validate_on_submit():
        user_email = form.user_email.data
        password = form.password.data

        user = Users.query.filter_by(user_email=user_email).first()

        if user:
            if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                flash("Login successful. Welcome!", 'success')
                session['user'] = user_email
                return redirect(url_for('blog.dashboard'))
            else:
                flash("Invalid Email or Password.", 'danger')

    return render_template('sign-in.html', form=form, parameters=parameters)


@bp.route('/sign_out')
def sign_out():
    if 'user' in session:
        session.pop('user')
        flash("You have been logged out successfully.", "success")
    return redirect(url_for('auth.signin'))
