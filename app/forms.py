from datetime import datetime, timedelta
import hashlib
from flask.globals import session
from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, HiddenField, \
    BooleanField, DateField, IntegerField, TimeField, RadioField
from wtforms.fields import SelectField
from wtforms.fields.simple import PasswordField, SubmitField
from wtforms.validators import DataRequired, ValidationError, Length, EqualTo, Email, NumberRange
from wtforms.widgets.core import TextArea

import re

from app.models import Discount, Location, PricingModel, User, UserDiscount
from config import HASH, HASH_ITERATION

def password_check(form, field):
    password = form.password.data
    if re.search('[0-9]', password) is None:
        raise ValidationError('Password must contain a number')
    elif re.search('[A-Z]', password) is None:
        raise ValidationError('Password must have one uppercase letter')

def username_check(form, field):
    username = form.username.data
    if User.query.filter_by(username=username).first() is not None:
        raise ValidationError('User with this username already exits')


class RegisterForm(FlaskForm):
    username = StringField('Username', validators = [
        DataRequired(),
        username_check
        ])
    password = PasswordField('Password', validators = [
        DataRequired(),
        password_check,
        Length(min = 8, max = 40, message = "password between 8 and 40 characters"),
        EqualTo('confirm', message = 'Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')    
    firstname = StringField('First Name', validators = [
        DataRequired(),
    ])

    email = EmailField('Email', validators = [
        DataRequired(),
        Email()
    ])
    phone_number = StringField('Phone Number')
    
    surname = StringField('Surname', validators = [
        DataRequired(),
    ])
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    username = StringField('Username', validators = [DataRequired()])
    password = PasswordField('Password', validators = [DataRequired()])

    submit = SubmitField('Log In')


class ForgotPasswordForm(FlaskForm):
    username = StringField('Username', validators = [
        DataRequired()
    ])
    email = EmailField('Email', validators = [
        DataRequired(),
        Email()
    ])
    submit = SubmitField('Remind Me!')


def authorization_check_password_change(form, field):
    password = form.old_password.data
    username = form.username.data
    hash_password = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'),HASH, HASH_ITERATION)

    if User.query.filter_by(username = username, password = hash_password).first() == None:
        raise ValidationError('Wrong Password!')

def authorization_check(form, field):
    password = form.password.data
    username = form.username.data
    hash_password = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'),HASH, HASH_ITERATION)

    if User.query.filter_by(username = username, password = hash_password).first() == None:
        raise ValidationError('Wrong Password!')


class ChangePasswordForm(FlaskForm):
    username = HiddenField("Username")
    old_password = PasswordField('Old Password', validators = [
        DataRequired(),
        authorization_check_password_change
    ])

    password = PasswordField('New Password', validators = [
        DataRequired(),
        password_check,
        Length(min = 8, max = 40, message = "password between 8 and 40 characters"),
        EqualTo('confirm', message = 'Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')    
    submit = SubmitField('Change')

class ChangeEmailForm(FlaskForm):
    username = HiddenField("Username")
    email = EmailField('Email', validators = [
        DataRequired(),
        Email()
    ])
    password = PasswordField('Password', validators = [
        DataRequired(),
        authorization_check
    ])
    submit = SubmitField('Change')


class FeedbackForm(FlaskForm):
    username = HiddenField("Username")
    title = StringField('Title', validators = [
        DataRequired()
    ])
    description = StringField('Description', widget=TextArea())
    high_priority = BooleanField('High Priority')
    submit = SubmitField('Send')



def card_number_check(form, field):
    card_number = form.card_number.data
    if len(card_number) != 16:
        raise ValidationError('Card Number must be 16 digits long!')
    try:
        int(card_number)
    except:
        raise ValidationError('Invalid Card Number!')


class PaymentMethodForm(FlaskForm):
    card_number = StringField(
        "Card Number",
        validators = [
            DataRequired(),
            card_number_check
        ] 
    )
    expiry_date = DateField("Expiry Date", format = '%y/%m')
    cvv = IntegerField(
        "CVV",
        validators = [
            DataRequired(),
            NumberRange(min=0, max=999)
        ]
    )

    card_holder_name = StringField("Card Holder Name", validators = [DataRequired()])
    card_holder_address_line_1 = StringField("Address Line 1", validators = [DataRequired()])
    card_holder_address_line_2 = StringField("Address Line 2", validators = [DataRequired()])
    card_holder_address_city = StringField("City", validators = [DataRequired()])
    card_holder_address_postal_code = StringField("Postal Code", validators = [DataRequired()])
    card_holder_address_country = StringField("Country", validators = [DataRequired()])

    save_card_details = BooleanField("Save Card Details for later")

    submit = SubmitField('Continue')


def valid_discount_code(form, field):
    code = form.discount_code.data
    if Discount.query.filter_by(code = code).first() == None:
        raise ValidationError("Invalid Code")


    if form.username.data in [ user_discount.user.username for user_discount in Discount.query.filter_by(code = code).first().users ]:
        raise ValidationError("Alerady Applied!")


class DiscountInputForm( FlaskForm ):
    username = HiddenField("Username")
    discount_code = StringField("Discount Code", validators = [
        DataRequired(),
        valid_discount_code
        ])
    submit = SubmitField('Apply Discount')


def in_the_future(form, field):
    pick_up_date = form.pick_up_date.data
    pick_up_time = form.pick_up_time.data
    today = datetime.date(datetime.today()) 
    pick_up_now = datetime.combine(pick_up_date, pick_up_time)
    if today > pick_up_date:
        raise ValidationError("Date can't be in the past!")
    elif datetime.now() > pick_up_now:
        raise ValidationError("Date can't be in the past!")


class ScooterBookingForm( FlaskForm ):
    # Pairs here: (id_of_location, name_of_location)
    pick_up_location = SelectField('Pick Up Location', choices = [(location.id, location.address) for location in Location.query.all()], validators = [DataRequired()])
    drop_off_location = SelectField('Drop Off Location', 
        choices = [(location.id, location.address) for location in Location.query.all()], 
        validators = [DataRequired()])
    # Pairs here: (id_of_pricing_model, representation of pricing model)
    pick_up_date = DateField('Pick Up Date', validators = [
        DataRequired(),
        in_the_future
    ])
    pick_up_time = TimeField("Pick Up time", validators = [
        DataRequired()
    ])
    ride_duration = SelectField('Ride Duration', 
        choices = [
            (pricing_model.id, pricing_model.__repr__()) for pricing_model in PricingModel.query.all()
        ], 
        validators = [
        DataRequired()
    ])

    submit = SubmitField('Confirm and pay')

class EmployeeScooterBookingForm( FlaskForm ):
    # Pairs here: (id_of_location, name_of_location)
    pick_up_location = SelectField('Pick Up Location', choices = [(location.id, location.address) for location in Location.query.all()], validators = [DataRequired()])
    drop_off_location = SelectField('Drop Off Location', 
        choices = [(location.id, location.address) for location in Location.query.all()], 
        validators = [DataRequired()])

    # Pairs here: (id_of_pricing_model, representation of pricing model)
    pick_up_date = DateField('Pick Up Date', validators = [
        DataRequired(),
        in_the_future
    ])
    pick_up_time = TimeField("Pick Up time", validators = [
        DataRequired()
    ])
    ride_duration = SelectField('Ride Duration', 
        choices = [
            (pricing_model.id, pricing_model.__repr__()) for pricing_model in PricingModel.query.all()
        ], 
        validators = [
        DataRequired()
    ])
    customer_name = StringField("Customer name", validators = [DataRequired()])
    customer_surname = StringField("Customer surname", validators = [DataRequired()])
    customer_email = EmailField('Email', validators = [
        DataRequired(),
        Email()
    ])

    submit = SubmitField('Confirm and pay')

class ExtendBookingForm( FlaskForm ):
    # Pairs here: (id_of_field, field)
    length = SelectField('Length', 
        choices = [
            (pricing_model.id, pricing_model.__repr__()) for pricing_model in PricingModel.query.all()
        ],
        validators = [DataRequired()]
    )

    submit = SubmitField('Extend')

def delete_permanently_validator(form, field):
    user_input = form.confirm.data
    if user_input != "delete permanently":
        raise ValidationError("Type in <i> delete permanently </i> to delete your account")

class ConfirmAccountDeletionForm( FlaskForm ):
    confirm = StringField('Confirm Deletion', validators = [
        DataRequired(),
        delete_permanently_validator
    ])
    submit = SubmitField('Delete')

def email_exists_validator(form, field):
    email = form.customer_email.data
    if User.query.filter_by(email = email).first() == None:
        raise ValidationError("User doesn't exist")

    
class EmailSearchForm( FlaskForm ):
    customer_email = EmailField('Email', validators = [
        DataRequired(),
        Email(),
        email_exists_validator
    ])
    submit = SubmitField('Submit')
    
class ManagerViewIncomeForm( FlaskForm ):
    # Pairs here: (id_of_location, name_of_location)
    hire_length = SelectField('Hire  Length', 
        choices = [(1, '1 hour'), (2, '4 hours'), (3, '1 day'), (4, '1 week'), (5, 'all')], 
        validators = [DataRequired()])
    choose_week = DateField("Choose the start of a week", validators = [
        DataRequired()
    ])

    submit = SubmitField('View Income')

class FindBookingForm( FlaskForm ):

    user_email = StringField("User Email")
    booking_id = StringField('Booking ID')
    user_id = StringField("User ID")
     

    submit = SubmitField('Search')

    def validate(self, extra_validators=None):
        if super().validate(extra_validators):

            if not (self.booking_id.data or self.user_email.data or self.user_id.data):
                self.user_id.errors.append('At least one field must have a value')
                return False
            else:
                return True
        return False


class FindIssueForm( FlaskForm ):

    issue_id = StringField('Booking ID')
    user_email = StringField("User Email")
    user_id = StringField("User ID")
    high_priority = BooleanField('High Priority')

    submit = SubmitField('Search')

class ScooterSearchForm( FlaskForm ):

    scooter_id = StringField('Scooter ID')
    active_flag = RadioField('Label', choices=[
        ('All','All'),
        ('Only Active','Only Active'),
        ('Only Inactive','Only Inactive')])

    submit = SubmitField('Search')


class PricingChangeForm( FlaskForm ):
    new_price = IntegerField('New Price', validators=[DataRequired()])
    submit = SubmitField('Confirm')
    