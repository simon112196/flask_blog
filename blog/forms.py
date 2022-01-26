
from email import message
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, EmailField, SelectField, FileField, RadioField, TextAreaField
from wtforms.validators import DataRequired, Regexp, ValidationError, EqualTo, Email, Length, Optional
from blog.models import User

class RegistrationForm(FlaskForm):
    first_name = StringField('First name',  validators=[DataRequired(message='First name is required.'), Regexp('^[a-zA-Z0-9]{1,20}$') ])
    password =PasswordField('Password', validators=[DataRequired(message='Password is required.'),  Regexp('^[a-zA-Z0-9]{6,20}$', message='Your password contains invalid character'), EqualTo('repeat_password', message='Password do not match. Please try again')])
    repeat_password = PasswordField('Confirm password', validators=[DataRequired(message='Please confirm your password.'), Regexp('^[a-zA-Z0-9]{6,20}$', message='Your password contains invalid character')])
    email = EmailField('Email', validators=[DataRequired(message='Email is required.'), Email(message='Invalid email. Please check'),Regexp("(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", message='Your email contains invalid character')])
    submit = SubmitField('Register')

    def validate_user(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Email already exist. Please choose a differenet one.')


class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Regexp('^[a-zA-Z0-9]{1,20}$') ])
    password = PasswordField('Password', validators=[DataRequired(), Regexp('^[a-zA-Z0-9]{1,20}$') ])
    submit = SubmitField('Login')

class CommentForm(FlaskForm):
    comment = TextAreaField('Comment', validators=[DataRequired(message='Write down your comment before submitting'), Length(min=0, max=2000, message='Number of word should not be over 2000.')])
    rating = RadioField('Rating', choices=[(5,''), (4,''), (3,''), (2,''), (1,'')], validators=[DataRequired(message='Rate before submitting.')])
    submit = SubmitField('Submit')


class PostForm(FlaskForm): 
    title = StringField('Title', validators=[DataRequired(), Length(min=1, max=50, message='Number of word should not be more than 50 words.')])
    content = TextAreaField('Content', validators=[DataRequired()])
    image_file = FileField('Image file', validators=[Optional(), Regexp('([^\s]+(\.(jpe?g|png|gif|bmp))$)]')])
    submit = SubmitField('Submit')


class SortForm(FlaskForm):
    order = SelectField('Order', choices=[('date_asc','Date Ascending'), ('date_desc','Date Descending')], validators=[DataRequired()])
    submit = SubmitField('Submit')