from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DecimalField, TextAreaField
from wtforms.validators import DataRequired


class PostForm(FlaskForm):
    title = StringField('Payment Owed To', validators=[DataRequired()])
    amount_due = DecimalField('Amount Due', default=0, places=2, validators=[DataRequired()])
    amount_paid = DecimalField('Amount Paid', default=0, places=2)
    date_due = StringField('Date Due')
    date_paid = StringField('Date Paid')
    paid_from = StringField('How Was The Bill Paid')
    confirmation = StringField('Payment Confirmation')
    content = TextAreaField('Notes')
    submit = SubmitField('Submit')
