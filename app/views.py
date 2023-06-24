from flask import render_template, url_for
from . import app, db
from .models import Users
from .utils import *
from .helper import *
from flask import session, redirect, request, session, render_template, flash, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, login_required, logout_user, current_user

app.jinja_env.globals.update(convert_datetime=convert_datetime, len = len, url_for=url_for, current_user=current_user, get_comment_likes_dislikes=get_comment_likes_dislikes, get_post_likes_dislikes=get_post_likes_dislikes)


@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if not username or not password:
            flash('Please Fill In Username/Password')
        else:
            user =  Users.query.filter_by(username=username).first()
            if not user:
                flash('Username Not Found', category='error')
            else:
                if (check_password_hash(user.password, password)):
                    login_user(user, remember=True)
                    return redirect(url_for('homepage'))
                else:      
                    flash('Password Is Incorrect', category='error')
                    return render_template('login.html', msg = 'Password Is Incorrect')      
    return render_template('login.html')
       
@app.route('/register',  methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        conformation = request.form.get('conformation')
        if not username or not password or not conformation:
            flash('Please fill in Username/Password/Conformation', category='error')
        else:
            if Users.query.filter_by(username=username).first():
                flash('Username Already Taken', category='error')
                return render_template('register.html', msg = 'Username Already Taken')
            else:
                if check_valid_password(password) == False:
                    flash('Invalid Password', category='error')
                elif conformation != password:
                    flash('Passwords Do not Match', category='error')
                elif len(username) > 18:
                    flash('Usernames Must Be 18 Characters Or Less', category='error')
                elif (' ' in username) == True:
                    flash('Username Can Not Contain Spaces', category='error')
                else:
                    user = insert_user(db, username, generate_password_hash(password)) 
                    login_user(user, remember=True)
                    return redirect(url_for('homepage'))             
    return render_template('register.html') 
 
@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')
     
@app.route('/')
@app.route('/homepage', methods = ['GET', 'POST'])
@login_required
def homepage():   
    posts = Posts.query.order_by(Posts.date.desc()).limit(10).all()
    session['currently_searching'] = None
    session['current_post_number'] = 10
    session['current_mode'] = "homepage"
    return render_template('homepage.html', posts=posts)

@app.route('/homepage/search', methods=['POST'])
@login_required
def search():
    search = request.form.get('search')
    if not search:
            return redirect('/homepage')
    session['currently_searching'] = search
    session['current_post_number'] = 10
    session['current_mode'] = "search"
    posts = Posts.query.filter(Posts.ts_vector.match(search)).limit(10).all()
    if len(posts) == 0:
        return render_template("no_valid_posts.html")
    else:
        return render_template('search.html', posts=posts)

@app.route('/myposts', methods=['GET'])
@login_required
def myposts():
    posts = Posts.query.filter(Posts.user_id == current_user.id).order_by(Posts.date.desc()).limit(10).all()
    session['currently_searching'] = None
    session['current_post_number'] = 10
    session['current_mode'] = "my_posts"
    return render_template('myposts.html', posts=posts)


@app.route('/more', methods=["POST"])
@login_required
def get_more():
    post_number = session['current_post_number']
    if session['current_mode'] == "search":
        search = session['currently_searching']
        posts = Posts.query.filter(Posts.ts_vector.match(search)).offset(post_number).limit(10).all()
    elif session['current_mode'] == "my_posts":
        posts = Posts.query.filter(Posts.user_id == current_user.id).order_by(Posts.date.desc()).offset(post_number).limit(10).all()
    else:
        posts = Posts.query.order_by(Posts.date.desc()).offset(post_number).limit(10).all()
    session['current_post_number'] = int(post_number) + 10
    return render_template("get_more_post.html", posts=posts)


@app.route('/post', methods=['GET', 'POST'])
@login_required
def post():
    if request.method == 'POST':
        title = request.form.get('title_for_post')
        text = request.form.get('text_for_post')
        if not title or not text:
            flash('Please Provide Title or Text', category='error')
        elif len(title) > 300:
            flash('Title has a 300 Character Limit', category='error')
        elif len(text) > 10000:
            flash('Post has a 10000 Character Limit', category='error')
        else:
            insert_post(db, title, text, current_user)
            return redirect(url_for('homepage'))
    return render_template('post.html')

@app.route('/blog_pages/<post_id>', methods=['GET', 'POST'])
@login_required
def get_blog_pages(post_id):
    post = Posts.query.filter_by(id=post_id).first()
    comments = Comments.query.filter_by(parent_id = None, post_id=post_id).all()
    commentlikedislike = db.session.query(UserComment).join(Comments).filter(Comments.post_id == post_id, UserComment.user_id == current_user.id).all()
    postlikeddislike = db.session.query(UserPost).filter(UserPost.post_id == post_id, UserPost.user_id == current_user.id).first()
    return render_template('blog_pages.html', post=post, current_user=current_user, comments=comments, commentlikedislike=commentlikedislike, postlikeddislike=postlikeddislike)
    
@app.route('/blog_pages/comment', methods=['POST'])
@login_required
def make_comment():
    req = request.get_json()
    post_id = int(req['postId'])
    comment_text = req['text']
    comment = insert_comment(db, current_user, post_id, comment_text)
    commentlikedislike = db.session.query(UserComment).filter(UserComment.comment_id == comment.id, UserComment.user_id == current_user.id).first()
    return render_template('get_more_comment.html', comment=comment, commentlikedislike=commentlikedislike)
    
    
@app.route('/blog_pages/reply_to_comments', methods=['POST'])
@login_required
def reply_to_comments():
    req = request.get_json()
    comment_text = req['text']
    parent_id = int(req['commentId'])
    comment_to_comment = insert_comment_to_comment(db,comment_text, parent_id, current_user)
    commentlikedislike = db.session.query(UserComment).filter(UserComment.comment_id == comment_to_comment.id, UserComment.user_id == current_user.id).first()
    return render_template('get_more_comment_to_comment.html', comment_to_comment=comment_to_comment, commentlikedislike=commentlikedislike)

@app.route('/blog_pages/comment/mode', methods=['POST'])
@login_required
def upvote_downvote_comment():
    req = request.get_json()
    comment_id = int(req['commentId'])
    mode = int(req['mode'])
    new_mode = insert_like_dislike_comment(db, current_user, comment_id, mode)
    like_dislike_value = get_comment_likes_dislikes(comment_id)
    return jsonify({"new_mode" : new_mode, "like_dislike_value" : like_dislike_value})

@app.route('/blog_pages/post/mode', methods=['POST'])
@login_required
def upvote_downvote_post():
    req = request.get_json()
    mode = int(req['mode'])
    post_id = int(req['postId'])
    new_mode = insert_like_dislike_post(db, current_user, post_id, mode)
    like_dislike_value = get_post_likes_dislikes(post_id)
    return jsonify({"new_mode" : new_mode, "like_dislike_value" : like_dislike_value})

@app.route('/blog_post/edit-comment', methods=['POST'])
@login_required
def edit_comment():
    req = request.get_json()
    comment_id = int(req['commentId'])
    text = req['text'] 
    edit_comment_text(comment_id, text)
    return jsonify({"text": text})

@app.route('/blog_post/delete', methods=['POST'])
@login_required
def delete_comment():
    req = request.get_json()
    comment_id = int(req['commentId'])
    check = delete_a_comment(comment_id)
    return jsonify({"check": check})