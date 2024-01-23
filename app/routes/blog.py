from flask import Flask, render_template, request, session, redirect, flash, url_for, Blueprint
from sqlalchemy.exc import SQLAlchemyError
from flask_caching import Cache
from app.models import Posts, Contacts, db
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
app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT='465',
    MAIL_USE_SSL=True,
    MAIL_USERNAME=parameters['gmail_username'],
    MAIL_PASSWORD=parameters['gmail_password']
)

mail = Mail(app)

bp = Blueprint("blog", __name__)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})


@bp.route("/")
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
        next_page = url_for('blog.home', page=page + 1)
    elif page == last:
        previous = url_for('blog.home', page=page - 1)
        next_page = "#"
    else:
        previous = url_for('blog.home', page=page - 1)
        next_page = url_for('blog.home', page=page + 1)

    return render_template('index.html', parameters=parameters, posts=posts_to_display,
                           previous=previous, next=next_page)


@bp.route("/about")
def about():
    return render_template('about.html', parameters=parameters, my_about=my_about)


@bp.route("/dashboard", methods=['GET', 'POST'])
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
    return redirect(url_for('auth.signin'))


@bp.route("/delete/<string:srl_num>", methods=['GET', 'POST'])
def delete(srl_num):
    if "user" in session:
        posts = Posts.query.filter_by(srl_num=srl_num).first()

        if posts:
            db.session.delete(posts)

            remaining_posts = Posts.query.order_by(Posts.srl_num).all()
            for idx, remaining_post in enumerate(remaining_posts, start=1):
                remaining_post.srl_num = idx

            db.session.commit()

            flash('Post deleted successfully', 'success')

    return redirect(url_for("blog.dashboard"))


@bp.route("/post/<string:post_slug>", methods=['GET'])
def post(post_slug):
    posts = Posts.query.filter_by(slug=post_slug).first()

    return render_template('post.html', parameters=parameters, post=posts)


@bp.route("/edit/<string:srl_num>", methods=['GET', 'POST'])
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
                flash("Post Added successfully.", "success")
                return redirect('/dashboard')
            else:
                posts = Posts.query.filter_by(srl_num=srl_num).first()
                posts.title = title
                posts.tagline = tagline
                posts.slug = slug
                posts.content = content
                posts.img_file = img_file
                posts.date = date
                db.session.commit()
                flash("Post updated successfully.", "success")
                return redirect('/dashboard')

        posts = Posts.query.filter_by(srl_num=srl_num).first()
        return render_template('edit.html', parameters=parameters, posts=posts, srl_num=srl_num)
    return redirect('/dashboard')

# Uploader Starts Here


ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@bp.route("/uploader", methods=['GET', 'POST'])
def uploader():
    if "user" in session:
        if request.method == 'POST':
            f = request.files['file1']
            if f and allowed_file(f.filename):
                f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
                flash("File uploaded successfully!", "success")
            else:
                flash("Invalid file format. Please upload a valid image file (jpg, jpeg, png, gif).", "error")
            return redirect(url_for('blog.dashboard'))


@bp.route("/contact", methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('message')

        if not name or not email or not phone or not message:
            flash('Please fill out all required fields.', 'warning')
            return redirect(url_for('blog.contact'))

        try:
            entry = Contacts(name=name, phone_num=phone, msg=message, date=datetime.now(), email=email)
            db.session.add(entry)
            db.session.commit()

            mail.send_message('New message from ' + name,
                              sender=email,
                              recipients=[parameters['gmail_username']],
                              body=message + "\n" + phone
                              )

            flash('Your message has been sent successfully!', 'success')
            return redirect(url_for('blog.contact'))

        except SQLAlchemyError as db_error:
            db.session.rollback()
            flash(f'Database error: {db_error}. Please try again later.', 'error')

        except Exception as other_error:
            flash(f'An unexpected error occurred: {other_error}. Please try again later.', 'error')

    return render_template('contact.html', parameters=parameters)
