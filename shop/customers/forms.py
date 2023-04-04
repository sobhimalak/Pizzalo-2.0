from wtforms import Form, StringField, TextAreaField, PasswordField,SubmitField,validators,ValidationError
from flask_wtf.file import FileRequired,FileAllowed, FileField
from flask_wtf import FlaskForm
from .models import Register



class CustomerRegisterForm(FlaskForm):
    name = StringField('Name')
    username = StringField('Username', [validators.DataRequired()])
    email = StringField('Email', [validators.Email(), validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired(), validators.EqualTo('confirm', message=' Both password must match! ')])
    confirm = PasswordField('Confirm Password', [validators.DataRequired()])
    country = StringField('Country', [validators.DataRequired()])
    city = StringField('City', [validators.DataRequired()])
    address = StringField('Address', [validators.DataRequired()])
    postal_code = StringField('Postal Code', [validators.DataRequired()])

    profile = FileField('Profile', validators=[FileAllowed(['jpg','png','jpeg','gif'], 'Image only please')])
    submit = SubmitField('Register')
    
    def validate_username(self, username):
        if Register.query.filter_by(username=username.data).first():
            raise ValidationError('Username is already taken!')
    def validate_name(self, name):
        if Register.query.filter_by(name=name.data).first():
            raise ValidationError('Name is already taken!')
        
    def validate_email(self, email):
        if Register.query.filter_by(email=email.data).first():
            raise ValidationError('Email is already registered!')
        
        
class CustomerLoginForm(FlaskForm):
    email = StringField('Email', [validators.Email(), validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired()])
    
