#! -*-coding:utf-8-*-
from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from .models import User


class LoginForm(Form):
    email = StringField(u'邮箱', validators=[Required(u'不能为空'), Length(1, 64), Email()])
    password = PasswordField(u'密码', validators=[Required(u'不能为空')])
    remember_me = BooleanField(u'保持登陆状态')
    submit = SubmitField(u'登陆')


class RegistrationForm(Form):
    email = StringField(u'邮箱', validators=[Required(u'不能为空'), Length(1, 64), Email()])
    username = StringField(u'用户名', validators=[
        Required(u'不能为空'), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, u'用户名由字母数字组成')])
    password = PasswordField(u'密码', validators=[
        Required(u'不能为空'), EqualTo('password2', message=u'两次输入的密码不一致')])
    password2 = PasswordField(u'确认密码', validators=[Required(u'不能为空')])
    submit = SubmitField(u'注册')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError(u'邮箱已被注册')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError(u'用户名已被使用')


class ChangePasswordForm(Form):
    old_password = PasswordField(u'旧密码', validators=[Required(u'不能为空')])
    password = PasswordField(u'新密码', validators=[
        Required(u'不能为空'), EqualTo('password2', message=u'两次输入的密码不一致')])
    password2 = PasswordField(u'确认新密码', validators=[Required(u'不能为空')])
    submit = SubmitField(u'确认修改')


class PasswordResetRequestForm(Form):
    email = StringField(u'邮箱', validators=[Required(u'不能为空'), Length(1, 64), Email()])
    submit = SubmitField(u'重置密码')


class PasswordResetForm(Form):
    email = StringField(u'邮箱', validators=[Required(u'不能为空'), Length(1, 64), Email()])
    password = PasswordField(u'新密码', validators=[
        Required(u'不能为空'), EqualTo('password2', message=u'两次输入的密码不一致')])
    password2 = PasswordField(u'确认新密码', validators=[Required(u'不能为空')])
    submit = SubmitField(u'确认修改')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first() is None:
            raise ValidationError(u'非法邮箱')


class ChangeEmailForm(Form):
    email = StringField(u'新邮箱', validators=[Required(u'不能为空'), Length(1, 64), Email()])
    password = PasswordField(u'密码', validators=[Required(u'不能为空')])
    submit = SubmitField(u'更新邮箱')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已被注册')
