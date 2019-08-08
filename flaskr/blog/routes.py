from flask import g, redirect, render_template, url_for
from werkzeug.exceptions import abort
from flask_login import current_user, login_required

from . import bp

from .forms import PostForm
from ..models import Post, User


@bp.route('/')
def index():
    posts = g.session.query(Post).join(User).order_by(Post.created.desc()).all()
    return render_template('blog/index.html', posts=posts)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    form = PostForm()

    if form.validate_on_submit():
        post = Post(author_id=current_user.id)
        form.populate_obj(post)
        g.session.add(post)
        return redirect(url_for('blog.index'))

    return render_template('blog/create.html', form=form)


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
    form = PostForm(obj=post)

    if form.delete.data:
        return redirect(url_for('blog.delete', id=id))

    if form.validate_on_submit():
        form.populate_obj(post)
        return redirect(url_for('blog.index'))

    return render_template('blog/update.html', form=form)


@bp.route('/<int:id>/delete', methods=('GET', 'POST'))
@login_required
def delete(id):
    post = get_post(id)
    form = PostForm(obj=post)
    
    if form.delete.data:
        g.session.delete(post)
        return redirect(url_for('blog.index'))
        
    return render_template('blog/delete.html', form=form)
