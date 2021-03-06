from flask import render_template, flash, redirect, url_for, request, jsonify
from app import app, db, socketio
from app.forms import LoginForm, RegistrationForm, EditProfileForm, EmptyForm, PostForm, ResetPasswordRequestForm, ResetPasswordForm, SendMessageForm
from app.models import User, Post, Message
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from datetime import datetime
from app.emails import send_password_reset_email
from app.schema import MessageSchema
from app.sockets import live_users
import json

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.post.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post is now live!')
        return redirect(url_for('index'))
    page = request.args.get('page', 1, type=int)
    posts=current_user.followed_posts().paginate(page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('index', page=posts.next_num) if posts.has_next else None
    prev_url = url_for('index', page=posts.prev_num) if posts.has_prev else None
    return render_template('index.html', title="Home Page", form=form, 
                            posts=posts.items, next_url=next_url, 
                            prev_url=prev_url)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        # print(user)
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page=url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratualtions, You are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', titl='Register', form=form)


@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    posts = user.posts.order_by(Post.timestamp.desc()).paginate(page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('user', username=user.username, page=posts.next_num) if posts.has_next else None
    prev_url = url_for('user', username=user.username, page=posts.prev_num) if posts.has_prev else None
    form = EmptyForm()
    post_del_form = EmptyForm()
    return render_template('user.html', user=user, posts=posts.items, 
                            next_url=next_url, prev_url=prev_url, form=form, post_del_form=post_del_form)


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username=form.username.data
        current_user.about_me = form.about_me.data
        current_user.location = form.location.data
        db.session.commit()
        flash('Your changes has been saved')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data=current_user.username
        form.about_me.data = current_user.about_me
        form.location.data = current_user.location
    return render_template('edit_profile.html', title='Edit Profile', form=form)
        

@app.route('/follow/<username>', methods=['POST'])
@login_required
def follow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash(f'User {username} not found.')
            return redirect(url_for('index'))
        if user==current_user:
            flash(f'You cannot follow yourself!')
            return redirect(url_for('user', username=username))
        current_user.follow(user)
        db.session.commit()
        flash(f'You are now following {username}')
        return redirect(url_for('user', username=username))
    else:
        return redirect(url_for('index'))


@app.route('/unfollow/<username>', methods=['POST'])
@login_required
def unfollow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash('User {} not found.'.format(username))
            return redirect(url_for('index'))
        if user == current_user:
            flash('You cannot unfollow yourself!')
            return redirect(url_for('user', username=username))
        current_user.unfollow(user)
        db.session.commit()
        flash('You are not following {}.'.format(username))
        return redirect(url_for('user', username=username))
    else:
        return redirect(url_for('index'))


@app.route('/explore')
@login_required
def explore():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('explore', page=posts.next_num) if posts.has_next else None
    prev_url = url_for('explore', page=posts.prev_num) if posts.has_prev else None
    return render_template('index.html', title='Explore', posts=posts.items, 
                            next_url=next_url, prev_url=prev_url)


@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Check your email for the instructions to reset your password')
        return redirect(url_for('login'))
    return render_template('reset_password_request.html', title='Reset Password', form=form)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user  = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)


@app.route('/delete/post/<post_id>', methods=['POST'])
@login_required
def delete_post(post_id):
    # form = EmptyForm()
    # post = Post.query.get(post_id)
    # if not post:
    #     return redirect(url_for('index'))
    # user = post.author
    # if not user or user != current_user:
    #     return redirect(url_for('index'))
    # db.session.delete(post)
    # db.session.commit()
    # return redirect(url_for('user', username=current_user.username))

    form = EmptyForm()
    if form.validate_on_submit():
        post = Post.query.get(post_id)
        if not post:
            return redirect(url_for('index'))
        user = post.author
        if not user or user != current_user:
            return redirect(url_for('index'))
        db.session.delete(post)
        db.session.commit()
        return redirect(url_for('user', username=current_user.username))
    return redirect(url_for('index'))


@app.route('/notifications')
@login_required
def notification():
    current_user.has_unseen_messages = 0
    db.session.commit()
    return render_template('notifications.html')

@app.route('/load-notifications')
@login_required
def load_notifications():
    page = request.args.get('page', 1, type=int)
    messages = current_user.get_received_messages().paginate(page, app.config['MESSAGES_PER_PAGE'], False)
    message_schema = MessageSchema(many=True)
    result = message_schema.dump(messages.items)

    for message in messages.items:
        if not message.seen_time:
            message.check_seen()
        db.session.commit()

    return jsonify({"messages": result, "hasNext": messages.has_next})


@app.route('/message/<recipient>', methods=['GET', 'POST'])
@login_required
def send_message(recipient):
    user = User.query.filter_by(username=recipient).first()
    if not user or not current_user.is_following(user):
        return redirect(url_for('index'))
    form = SendMessageForm()
    return render_template('send_message.html', form=form, recipient=recipient)


@app.route('/send-message/<recipient>', methods=['POST'])
def send_message_action(recipient):
    form = SendMessageForm()
    if form.validate_on_submit():
        recipient = User.query.filter_by(username=recipient).first()
        msg = Message(content=form.content.data, sender=current_user, recipient=recipient)
        db.session.add(msg)
        recipient.has_unseen_messages = 1
        db.session.commit()
        newMsg = Message.query.get(msg.id)
        flash("Your message has been send")
        message_schema = MessageSchema()
        result = message_schema.dump(newMsg)
        if recipient.username in live_users:
            socketio.emit('new messages', {"msg": "You have a new message"}, room=live_users[recipient.username])
            socketio.emit('notification_alert', result, room=live_users[recipient.username], callback=ack)
        return redirect(url_for('send_message', recipient=recipient.username))


def ack(msg, data):
    if msg == 'success':
        message = Message.query.get(data)
        message.check_seen()
        message.recipient.has_unseen_messages=0
        db.session.commit()



################
################
@app.route('/socket-template')
def socket_template():
    return render_template('sockets.html')