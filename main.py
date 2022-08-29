from flask import Flask, render_template, request, redirect, url_for, flash, abort
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email
import os

# TODO: create images, replace placeholders

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
Bootstrap(app)


class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()], render_kw={"placeholder": "Name"})
    email = EmailField('Email', validators=[DataRequired(), Email()], render_kw={"placeholder": "Email"})
    message = TextAreaField('Message', validators=[DataRequired()], render_kw={"placeholder": "Message"})
    submit = SubmitField('Send Message')


@app.route('/', methods=["POST", "GET"])
def index():
    form = ContactForm()
    return render_template('index.html', form=form)


if __name__ == "__main__":
    app.run(debug=True)
