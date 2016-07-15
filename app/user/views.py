#! -*-coding:utf-8-*-
from flask import render_template, redirect, request, url_for, flash
from flask.ext.login import login_user, logout_user, login_required, current_user
from . import user
from .. import db
from .models import User
from .email import send_email
from .forms import LoginForm, RegistrationForm, ChangePasswordForm, PasswordResetRequestForm, PasswordResetForm, ChangeEmailForm


@user.before_app_request
def before_request():
    if current_user.is_authenticated \
            and not current_user.confirmed \
            and request.endpoint[:5] != 'user.' \
            and request.endpoint != 'static':
        return redirect(url_for('user.unconfirmed'))


@user.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    flash(u'当前用户未激活')
    return render_template('user/unconfirmed.html')


@user.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash(u'用户名或密码错误')
    return render_template('user/login.html', form=form)


@user.route('/logout')
@login_required
def logout():
    logout_user()
    flash(u'成功登出')
    return redirect(url_for('main.index'))


@user.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        send_email(user.email, 'Confirm Your Account',
                   'user/email/confirm', user=user, token=token)
        flash(u'激活邮件已经发送，请到你邮箱中查看并激活')
        return redirect(url_for('user.login'))
    return render_template('user/register.html', form=form)


@user.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        flash(u'已经激活你的账号')
    else:
        flash(u'激活链接已失效')
    return redirect(url_for('main.index'))


@user.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, u'激活你的账号',
               'user/email/confirm', user=current_user, token=token)
    flash(u'新的激活邮件以发送到您的邮箱')
    return redirect(url_for('main.index'))


@user.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.password.data
            db.session.add(current_user)
            flash(u'成功修改你的密码')
            return redirect(url_for('main.index'))
        else:
            flash(u'无效的密码')
    return render_template("user/change_password.html", form=form)


@user.route('/reset', methods=['GET', 'POST'])
def password_reset_request():
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            token = user.generate_reset_token()
            send_email(user.email, u'重置你的密码',
                       'user/email/reset_password',
                       user=user, token=token,
                       next=request.args.get('next'))
            flash(u'重置密码的邮件已发送至你的邮箱')
        else:
            flash(u'邮箱不存在')
        return redirect(url_for('user.login'))
    return render_template('user/reset_password.html', form=form)


@user.route('/reset/<token>', methods=['GET', 'POST'])
def password_reset(token):
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = PasswordResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            return redirect(url_for('main.index'))
        if user.reset_password(token, form.password.data):
            flash(u'密码已被重置')
            return redirect(url_for('user.login'))
        else:
            return redirect(url_for('main.index'))
    return render_template('user/reset_password.html', form=form)


@user.route('/change-email', methods=['GET', 'POST'])
@login_required
def change_email_request():
    form = ChangeEmailForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.password.data):
            new_email = form.email.data
            token = current_user.generate_email_change_token(new_email)
            send_email(new_email, u'激活你的账户',
                       'user/email/change_email',
                       user=current_user, token=token)
            flash(u'邮件成功发送')
            return redirect(url_for('main.index'))
        else:
            flash(u'无效的邮箱或密码')
    return render_template("user/change_email.html", form=form)


@user.route('/change-email/<token>')
@login_required
def change_email(token):
    if current_user.change_email(token):
        flash(u'你的邮箱地址已被更新')
    else:
        flash(u'无效的请求')
    return redirect(url_for('main.index'))
