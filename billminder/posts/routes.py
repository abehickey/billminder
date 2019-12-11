from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from billminder import db
from billminder.models import Post
from billminder.posts.forms import PostForm

posts = Blueprint('posts', __name__)


@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, amount_due=form.amount_due.data, date_due=form.date_due.data, amount_paid=form.amount_paid.data,
                    date_paid=form.date_paid.data, paid_from=form.paid_from.data, confirmation=form.confirmation.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your bill has been created!', 'success')
        return redirect(url_for('users.home'))
    print(form.validate_on_submit())
    return render_template('create_post.html', title='Add New Bill', form=form, legend='Add New Bill')


@posts.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.date_due = form.date_due.data
        post.amount_due = form.amount_due.data
        post.amount_paid = form.amount_paid.data
        post.date_paid = form.date_paid.data
        post.paid_from = form.paid_from.data
        post.confirmation = form.confirmation.data
        post.content = form.content.data
        db.session.commit()
        flash('Your Bill has been updated!', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.date_due.data = post.date_due
        form.amount_due.data = post.amount_due
        form.date_paid.data = post.date_paid
        form.amount_paid.data = post.amount_paid
        form.paid_from.data = post.paid_from
        form.confirmation.data = post.confirmation
        form.content.data = post.content
    return render_template('create_post.html', title='Update Bill',
                           form=form, legend='Update Bill')


@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your Bill has been deleted!', 'success')
    return redirect(url_for('users.home'))
