from flask import (
    flash, g, redirect, render_template, request, url_for, abort
)
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, logout_user, login_required
from is_safe_url import is_safe_url

from . import bp

from ..models import User


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif g.session.query(User).filter_by(username=username).first():
            error = 'User {} is already registered.'.format(username)

        if not error:
            g.session.add(
                User(
                    username=username,
                    password=generate_password_hash(password)
                )
            )
            return redirect(url_for('auth.login'))

        flash(error)
    
    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None
        user = g.session.query(User).filter_by(username=username).first()

        if not user:
            error = 'Incorrect username.'
        elif not check_password_hash(user.password, password):
            error = 'Incorrect password.'

        if not error:
            login_user(user)
            url = request.args.get('next', url_for('index'))
            if not is_safe_url(url, allowed_hosts={''}):
                return abort(400)
            return redirect(url)

        flash(error)

    return render_template('auth/login.html')


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))
