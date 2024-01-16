from flask import Flask, render_template, request, session, redirect, flash, url_for
from sqlalchemy.exc import SQLAlchemyError
from forms import SignupForm, SigninForm
import bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
import json
from datetime import datetime
import math
import os
from werkzeug.utils import secure_filename

with open('config.json', 'r') as c:
    parameters = json.load(c)["parameters"]
with open('config.json', 'r') as c:
    my_about = json.load(c)["my_about"]

local_server = True

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = parameters['upload_location']
app.secret_key = 'super-secret-key'
app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT='465',
    MAIL_USE_SSL=True,
    MAIL_USERNAME=parameters['gmail_username'],
    MAIL_PASSWORD=parameters['gmail_password']
)
mail = Mail(app)
if local_server:
    app.config["SQLALCHEMY_DATABASE_URI"] = parameters['local_uri']
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = parameters['production_uri']
db = SQLAlchemy(app)


# Schemas starts here
class Users(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(80), nullable=False)
    user_email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)


class Contacts(db.Model):
    srl_num = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(20), nullable=False)
    phone_num = db.Column(db.String(12), nullable=False)
    msg = db.Column(db.String(150), nullable=False)
    date = db.Column(db.String(12), nullable=True)


class Posts(db.Model):
    srl_num = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    tagline = db.Column(db.String(50), nullable=False)
    slug = db.Column(db.String(30), nullable=False)
    content = db.Column(db.String(150), nullable=False)
    date = db.Column(db.String(12), nullable=True)
    img_file = db.Column(db.String(12), nullable=True)


with app.app_context():
    # Create tables based on the models
    db.create_all()


@app.route("/signup", methods=['GET', 'POST'])
def sign_up():
    form = SignupForm()
    if form.validate_on_submit():
        user_name = form.user_name.data
        user_email = form.user_email.data
        password = form.password.data

        existing_user = Users.query.filter_by(user_email=user_email).first()

        if existing_user:
            flash("User with this Email already exists. Please use a different email.", 'warning')
            return redirect(url_for('sign_up'))
        else:
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            # store data into database
            entry = Users(user_name=user_name, user_email=user_email, password=hashed_password)
            db.session.add(entry)
            db.session.commit()
            flash("Sign up successful.")

        return redirect(url_for('signin'))

    return render_template('sign-up.html', form=form, parameters=parameters)


@app.route('/signin', methods=['GET', 'POST'])
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
                return redirect(url_for('dashboard'))
            else:
                flash("Incorrect password. Please try again with the correct password.", 'danger')
        else:
            flash("User not found with this email. Please check your email and try again.", 'danger')

    return render_template('sign-in.html', form=form, parameters=parameters)


@app.route('/sign_out')
def sign_out():
    if 'user' in session:
        session.pop('user')
        flash("You have been logged out successfully.", "success")
    return redirect('/signin')


@app.route("/")
def home():
    posts = Posts.query.filter_by().all()
    last = math.ceil(len(posts) / int(parameters['no_of_posts']))
    page = request.args.get('page')

    if not str(page).isnumeric():
        page = 1
    page = int(page)

    start_index = (page - 1) * int(parameters['no_of_posts'])
    end_index = start_index + int(parameters['no_of_posts'])

    posts_to_display = posts[start_index:end_index]

    if page == 1:
        previous = "#"
        next_page = "/?page=" + str(page + 1)
    elif page == last:
        previous = "/?page=" + str(page - 1)
        next_page = "#"
    else:
        previous = "/?page=" + str(page - 1)
        next_page = "/?page=" + str(page + 1)

    return render_template('index.html', parameters=parameters, posts=posts_to_display,
                           previous=previous, next=next_page)


@app.route("/about")
def about():
    return render_template('about.html', parameters=parameters, my_about=my_about)


@app.route("/dashboard", methods=['GET', 'POST'])
def dashboard():
    if 'user' in session:
        posts = Posts.query.all()
        return render_template('dashboard.html', parameters=parameters, posts=posts)
    if request.method == 'POST':
        user_email = request.form.get('user_email')
        password = request.form.get('password')
        if user_email == 'user_email' and password == 'password':
            session['user'] = user_email
            posts = Posts.query.all()
            return render_template('dashboard.html', parameters=parameters, posts=posts)

    flash("Please sign in to access the dashboard.", 'danger')
    return redirect(url_for('signin'))


@app.route("/delete/<string:srl_num>", methods=['GET', 'POST'])
def delete(srl_num):
    if "user" in session:
        posts = Posts.query.filter_by(srl_num=srl_num).first()
        db.session.delete(posts)
        db.session.commit()
    return redirect("/dashboard")


@app.route("/post/<string:post_slug>", methods=['GET'])
def post(post_slug):
    posts = Posts.query.filter_by(slug=post_slug).first()

    return render_template('post.html', parameters=parameters, post=posts)


#  Reset the auto-increment counter to a specific value (e.g., 1)
# ALTER TABLE your_table AUTO_INCREMENT = 1;


@app.route("/edit/<string:srl_num>", methods=['GET', 'POST'])
def edit(srl_num):
    if "user" in session:
        if request.method == "POST":
            title = request.form.get('title')
            tagline = request.form.get('tagline')
            slug = request.form.get('slug')
            content = request.form.get('content')
            img_file = request.form.get('img_file')
            date = datetime.now()

            if srl_num == '0':
                posts = Posts(title=title, slug=slug, content=content, tagline=tagline, img_file=img_file, date=date)
                db.session.add(posts)
                db.session.commit()
            else:
                posts = Posts.query.filter_by(srl_num=srl_num).first()
                posts.title = title
                posts.tagline = tagline
                posts.slug = slug
                posts.content = content
                posts.img_file = img_file
                posts.date = date
                db.session.commit()
                return redirect('/edit/' + srl_num)

        posts = Posts.query.filter_by(srl_num=srl_num).first()
        return render_template('edit.html', parameters=parameters, posts=posts, srl_num=srl_num)
    return redirect('/dashboard')


# Uploader Starts Here


ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/uploader", methods=['GET', 'POST'])
def uploader():
    if "user" in session:
        if request.method == 'POST':
            f = request.files['file1']
            if f and allowed_file(f.filename):
                f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
                flash("File uploaded successfully!", "success")
            else:
                flash("Invalid file format. Please upload a valid image file (jpg, jpeg, png, gif).", "error")
            return redirect(url_for('dashboard'))


@app.route("/contact", methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # Fetch data from the form
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('message')

        # Check if any of the required fields is empty
        if not name or not email or not phone or not message:
            flash('Please fill out all required fields.', 'warning')
            return redirect(url_for('contact'))

        try:
            # Add entry to the database
            entry = Contacts(name=name, phone_num=phone, msg=message, date=datetime.now(), email=email)
            db.session.add(entry)
            db.session.commit()

            # Send email
            mail.send_message('New message from ' + name,
                              sender=email,
                              recipients=[parameters['gmail_username']],
                              body=message + "\n" + phone
                              )

            # Display a success flash message
            flash('Your message has been sent successfully!', 'success')

            # Redirect to the contact page
            return redirect(url_for('contact'))

        except SQLAlchemyError as db_error:
            # Handle database-related exceptions
            db.session.rollback()
            flash(f'Database error: {db_error}. Please try again later.', 'error')

        except Exception as other_error:
            # Handle other exceptions
            flash(f'An unexpected error occurred: {other_error}. Please try again later.', 'error')

    return render_template('contact.html', parameters=parameters)


if __name__ == '__main__':
    app.run(debug=True)
