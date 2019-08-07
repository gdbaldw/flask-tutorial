from flask import (
    flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from flask_login import current_user

from . import bp

from flask_login import login_required

from ..models import Post, User


@bp.route('/')
def index():
    posts = g.session.query(Post).join(User).order_by(Post.created.desc()).all()
    return render_template('blog/index.html', posts=posts)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']

        error = None if title else 'Title is required.'

        if error:
            flash(error)
        else:
            g.session.add(Post(title=title, body=body, author_id=current_user.id))
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')


def get_post(id, check_author=True):
    post = g.session.query(Post).filter_by(id=id).join(User).first()

    if post is None:
        abort(404, "Post id {} doesn't exist.".format(id))

    if check_author and post.author.id != current_user.id:
        abort(403)

    return post


@bp.route('<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        
        error = None if title else 'Title is required.'

        if error:
            flash(error)
        else:
            post.title = title
            post.body = body
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    post = get_post(id)
    g.session.delete(post)
    return redirect(url_for('blog.index'))
