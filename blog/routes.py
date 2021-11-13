from logging import log
from flask.helpers import flash
from flask_login.utils import login_required, login_user, logout_user
from blog import app, db
from flask import render_template, url_for
from blog.models import BlogPost, Comment, Portfolio, User
from blog.forms import CommentForm, EditForm, LoginForm, PortfolioForm, BlogForm, LoginForm
from flask_login import login_user
import os
from werkzeug.utils import redirect
from datetime import datetime
from sqlalchemy import desc



ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('index.html')





@app.route('/login', methods = ['POST', 'GET'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email_username.data).first()
        if user and user.verify_password(form.password.data):
            login_user(user)
            return redirect(url_for('home_page'))
        
    return render_template('login.html', form = form)




@app.route('/logout')
def logout():
    logout_user()
    return redirect (url_for('home_page'))



@app.route('/blog', methods= ['GET','POST'])
def blog_page():
    blogposts = BlogPost.query.order_by(desc(BlogPost.id)).all()
    return render_template('blog.html', blogposts = blogposts)




@app.route('/addblog', methods = ['POST','GET'])
@login_required
def add_blog():
    form = BlogForm()
    if form.validate_on_submit():
        if allowed_file(form.image.data.filename):
            form.image.data.save(os.path.join(app.config['UPLOAD_FOLDER'], form.image.data.filename))
            form.back_image.data.save(os.path.join(app.config['UPLOAD_FOLDER'], form.image.data.filename))
            b1 = BlogPost(title = form.title.data, subtitle = form.subtitle.data, body = form.body.data, image_name = form.image.data.filename, back_image_name = form.back_image.data.filename, date = datetime.now().strftime('%a %d, %B, %y'))
            db.session.add(b1)
            db.session.commit()
            flash(f'Post successfully added bro', category='success')
            return redirect(url_for('blog_page'))
    if form.errors != {}:
        for err in form.errors.values():
            flash(f'There was this error {err} while creating the blog post', category='danger')
         
    return render_template('add_blog.html', form = form)


@app.route('/portfolio')
def portfolio_page():
    ports = Portfolio.query.all()
    return render_template('portfolio.html',ports=ports)



@app.route('/addportfolio', methods = ['GET', 'POST'])
@login_required
def add_portfolio_page():
    form = PortfolioForm()
    if form.validate_on_submit():
        p1 = Portfolio(title = form.title.data, link = form.link.data, github = form.github.data )
        db.session.add(p1)
        db.session.commit()
        return redirect(url_for("portfolio_page"))
    if form.errors != {}:
        for err in form.errors.values():
            flash(f'There was this error {err} while creating the blog post', category='danger')
    return render_template('addportfolio.html',form=form)




@app.route('/blog/<blog_id>', methods = ['POST', 'GET'])
def read_post(blog_id):
    blog = BlogPost.query.filter_by(id =int( blog_id)).first()
    old_comments = Comment.query.filter_by(owner = blog.id).all()

    new_comment = CommentForm()
    if new_comment.validate_on_submit():
        c1 = Comment(name = new_comment.name.data, date = datetime.now().strftime('%a %d, %B, %y'), body = new_comment.body.data, owner = blog.id)
        db.session.add(c1)
        db.session.commit()
        return redirect(url_for('read_post', blog_id = blog.id))

    return render_template('read_blog.html', blog = blog,  old_comments = old_comments, new_comment = new_comment)

@app.route('/about')
def about_page():
    return render_template('about.html')


@app.route('/edit/<id>', methods = ['POST', 'GET'])
@login_required
def edit_post(id):
    post = BlogPost.query.filter_by(id = id).first()
    
    form = EditForm()

    if form.validate_on_submit():
        
        post.body = form.body.data
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('blog_page'))

    return render_template('edit_blog.html', form = form, post = post)

@app.route('/delete/<id>', methods = ['POST', 'GET'])
@login_required
def delete_post(id):
    post = BlogPost.query.filter_by(id = id).first()
    comments = Comment.query.filter_by(owner = id).first()
    db.session.delete(post)
    db.session.delete(comments)
    db.session.commit()
    return redirect(url_for('blog_page'))

@app.route('/delete_comment/<id>', methods = ['POST', 'GET'])
@login_required
def delete_comment(id):
    post = Comment.query.filter_by(id = id).first()
    db.session.delete(post)
    db.session.commit()
    flash('Successfuly deleted comment', category='success')
    return redirect(url_for('read_post', blog_id= post.owner))

