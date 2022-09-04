from flask import Flask, render_template, request, redirect, url_for, flash, abort
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from flask_mail import Mail, Message
from wtforms import StringField, EmailField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email
import os

# TODO: create images, replace placeholders
# TODO: Implement Feedback for email successfully sent

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
Bootstrap(app)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = os.environ.get('FORM_EMAIL')
app.config['MAIL_PASSWORD'] = os.environ.get('GMAIL_APP_PASSWORD')
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)


class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()], render_kw={"placeholder": "Name"})
    email = EmailField('Email', validators=[DataRequired(), Email()], render_kw={"placeholder": "Email"})
    message = TextAreaField('Message', validators=[DataRequired()], render_kw={"placeholder": "Message"})
    submit = SubmitField('Send Message')


@app.route('/', methods=["POST", "GET"])
def index():
    form = ContactForm()
    if form.validate_on_submit():
        msg = Message(
            subject=f'{form.name.data} sent you a message! Email: {form.email.data}',
            sender=os.environ.get('FORM_EMAIL'),
            recipients=[os.environ.get('FORM_EMAIL')]
        )
        msg.body = form.message.data
        mail.send(msg)
        return redirect(url_for('index')+'#contact')
    return render_template('index.html', form=form)


@app.route('/portfolio', methods=["POST", "GET"])
def portfolio():
    return render_template('portfolio.html')


if __name__ == "__main__":
    app.run(debug=True)
