from flask import g, redirect, render_template, request, url_for, abort
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash
from is_safe_url import is_safe_url

from . import bp

from .forms import LoginForm, RegistrationForm
from ..models import User


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        g.session.add(
            User(
                username=request.form['username'],
                password=generate_password_hash(
                    request.form['password']
                )
            )
        )
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        login_user(
            g.session.query(User).filter_by(
                username=form.username.data
            ).first(),
            remember=form.remember_me.data
        )
        url = request.args.get('next', url_for('index'))
        if not is_safe_url(url, allowed_hosts={''}):
            return abort(400)
        return redirect(url)
    return render_template('auth/login.html', form=form)


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))
