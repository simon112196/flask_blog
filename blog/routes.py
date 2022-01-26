from flask import render_template, url_for, redirect, flash
from flask_login.utils import logout_user
from blog import app, db
from blog.models import User, Post, Comment
from blog.forms import CommentForm, RegistrationForm, LoginForm, SortForm, PostForm
from flask_login import login_user, current_user
from sqlalchemy import desc, asc
# @app.route("/")

@app.route("/home", methods=['GET', 'POST'])
def home():
    form_sort = SortForm()
    form = PostForm()
    posts = Post.query.order_by(desc(Post.date)).all()
    if form_sort.validate_on_submit():
        if form_sort.order.data == 'date_desc':
            posts = Post.query.order_by(desc(Post.date)).all()
            return render_template('home.html', posts=posts, title='Home', form_sort=form_sort, form=form)
        elif form_sort.order.data == 'date_asc':
            posts = Post.query.order_by(asc(Post.date)).all()
            return render_template('home.html', posts=posts, title='Home', form_sort=form_sort, form=form)
        

    '''if form.validate_on_submit():
        if current_user.is_authenticated:
            post = Post(title=form.title.data, content=form.content.data,image_file=form.image_file.data, author_id=current_user.id)

            db.session.add(post)
            db.session.commit()
            flash("Blog is successfully uploaded!")
            return redirect(url_for('home'))
        else:
            flash("Login before uploading!")'''

        
    return render_template('home.html', posts=posts, title='Home', form_sort=form_sort, form=form)

@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/post/<int:post_id>", methods=['GET', 'POST'])
def post(post_id):
    form = CommentForm()
    post = Post.query.get_or_404(post_id)
    comments = Comment.query.filter_by(post_id=post_id).order_by(desc(Comment.date)).all()

    if form.validate_on_submit():
        if current_user.is_authenticated:
            comment = Comment(post_id=post_id, author_id=current_user.get_id(), comment=form.comment.data, rating=form.rating.data)
            post_rate = post.avr_rate * post.rate_cnt + int(comment.rating)
            post.rate_cnt += 1
            post.avr_rate = round(post_rate/post.rate_cnt, 2)
            db.session.add(comment)
            db.session.commit()
            return redirect(url_for('post', post_id=post.id))
        else:
            flash("Please login!")
    
    return render_template('post.html', title=post.title, post=post, comments=comments, form=form)

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    try:
        user_email = User.query.filter_by(email=form.email.data).first()
        if user_email is None:
            if form.validate_on_submit():
                user = User(first_name=form.first_name.data, password=form.password.data, email=form.email.data)
                db.session.add(user)
                db.session.commit()
                flash("Registration successful!")
                login_user(user)
                return redirect(url_for('registered'))
        else:
            flash("Email already exist, try again with another email.")

    except :
        flash("Sorry, there is problem with your registration")
        return redirect(url_for('register'))
    return render_template('register.html', title='Register', form=form)

@app.route("/registered")
def registered():
    return render_template('registered.html', title='Thank you for registration')

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            flash("Welcome back," + " " + current_user.first_name + "!")
            return redirect(url_for('home'))
        flash("Incorrect email or password suppiled.")
    return render_template('login.html', title='Login', form=form)
    

@app.route("/logout")
def logout():
    logout_user()
    flash("You have been logged out")
    return redirect(url_for('home'))


