from flask_login import login_user, logout_user

from app.forms.auth import RegisterForm, LoginForm, EmailForm, ResetPasswordForm

from app.models.base import db
from app.models.user import User
from . import web
from flask import request, render_template, redirect, url_for, flash


@web.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        with db.auto_commit():
            user = User()
            user.set_attrs(form.data)
            db.session.add(user)
            # db.session.commit()
        return redirect(url_for('web.login'))
    return render_template('auth/register.html', form=form)


@web.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=True)    # 保存票据,写入到cookie中
            next = request.args.get('next')
            if not next or not next.startswith('/'):
                next = url_for('web.index')
            return redirect(next)
        else:
            flash('账号不存在或密码错误')
    return render_template('auth/login.html', form=form)


@web.route('/reset/password', methods=['GET', 'POST'])
def forget_password_request():
    form = EmailForm(request.form)
    if request.method == 'POST' and form.validate():
        # first_or_404 如果账户不存在会返回提示not found 抛出的异常是HttpExcepton的子类
        # 这里可以使用try except自定义异常信息，但是太啰嗦，在web 初始化里定义一个方法来处理
        user = User.query.filter_by(email=form.email.data).first_or_404()
        from app.libs.email import send_mail
        send_mail(form.email.data, '重置你的密码', 'email/reset_password.html',
                  user=user, token=user.generate_token())
    return render_template('auth/forget_password_request.html', form=form)


@web.route('/reset/password/<token>', methods=['GET', 'POST'])
def forget_password(token):
    form = ResetPasswordForm(request.form)
    if request.method == 'POST' and form.validate():
        result = User.reset_password(token, form.password1.data)
        if result:
            flash('密码重置成功，请使用新密码登录')
            return redirect(url_for('web.login'))
        else:
            flash('密码重置失败')
    return render_template('auth/forget_password.html', form=form)


@web.route('/change/password', methods=['GET', 'POST'])
def change_password():
    pass


@web.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('web.index'))
