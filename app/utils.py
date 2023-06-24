from .models import *

def insert_user(db, username, password):
    user = Users(username=username, password=password)
    db.session.add(user)
    db.session.commit()
    return user

def insert_post(db, title, text, current_user):
    new_post = Posts(title=title, text=text, user=current_user)
    db.session.add(new_post)
    db.session.commit()
    return new_post
    
def insert_comment(db, current_user, post_id, text):
    post = Posts.query.filter_by(id=post_id).first()
    new_comment = Comments(text=text, post=post, user=current_user)
    db.session.add(new_comment)
    db.session.commit()
    return new_comment

def insert_comment_to_comment(db, text, parent_id, current_user):
    parent = Comments.query.filter_by(id=parent_id).first()
    new_comment = Comments(text=text, parent=parent, post=parent.post,user=current_user)
    db.session.add(new_comment)
    db.session.commit()
    return new_comment

def insert_like_dislike_comment(db, current_user, comment_id, mode):
    comment_user_to_update = db.session.query(UserComment).filter(UserComment.user_id == current_user.id, UserComment.comment_id == comment_id).first()
    if comment_user_to_update == None:
        comment = Comments.query.filter_by(id=comment_id).first()
        comment_user = UserComment(user=current_user, comment=comment, mode=mode)
        db.session.add(comment_user)
        db.session.commit()
        return mode
    else:
        if comment_user_to_update.mode != mode:
            comment_user_to_update.mode = mode
        else:
            comment_user_to_update.mode = 0
        db.session.add(comment_user_to_update)
        db.session.commit()
    return comment_user_to_update.mode

def get_comment_likes_dislikes(comment_id):
        likes = len(db.session.query(UserComment).filter(UserComment.comment_id == comment_id, UserComment.mode == 1).all())
        dislikes = len(db.session.query(UserComment).filter(UserComment.comment_id == comment_id, UserComment.mode == 2).all())
        return likes - dislikes
    
def insert_like_dislike_post(db, current_user, post_id, mode):
    post_user_to_update = db.session.query(UserPost).filter(UserPost.user_id == current_user.id, UserPost.post_id == post_id).first()
    if post_user_to_update == None:
        post = Posts.query.filter_by(id=post_id).first()
        post_user = UserPost(user=current_user, post=post, mode=mode)
        db.session.add(post_user)
        db.session.commit()
        return mode
    else:
        if post_user_to_update.mode != mode:
            post_user_to_update.mode = mode
        else:
            post_user_to_update.mode = 0
        db.session.add(post_user_to_update)
        db.session.commit()
    return post_user_to_update.mode

def get_post_likes_dislikes(post_id):
    likes = len(db.session.query(UserPost).filter(UserPost.post_id == post_id, UserPost.mode == 1).all())
    dislikes = len(db.session.query(UserPost).filter(UserPost.post_id == post_id, UserPost.mode == 2).all())
    return likes - dislikes

def edit_comment_text(comment_id, text):
    comment = Comments.query.filter_by(id=comment_id).first()
    comment.text = text
    db.session.add(comment)
    db.session.commit()
    
#false means deletion of comment failed because that comment had children
def delete_a_comment(comment_id):
    comment = Comments.query.filter_by(id=comment_id).first()
    if (len(comment.replies.all()) == 0):
       db.session.delete(comment)
       db.session.commit()
       return True 
    else:
        return False