from flask import Flask, render_template, request, redirect, url_for, flash, abort
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from flask_mail import Mail, Message
from wtforms import StringField, EmailField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email
from morse_translator import translate
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


class MorseForm(FlaskForm):
    input_field = TextAreaField('Input Field',
                                validators=[DataRequired()],
                                render_kw={"placeholder": "Enter the text you would like translated into Morse Code"}
                                )
    submit = SubmitField('Translate My Text')


@app.route('/', methods=["POST", "GET"])
def index():
    contact_form = ContactForm()
    if contact_form.validate_on_submit():
        msg = Message(
            subject=f'{contact_form.name.data} sent you a message! Email: {contact_form.email.data}',
            sender=os.environ.get('FORM_EMAIL'),
            recipients=[os.environ.get('FORM_EMAIL')]
        )
        msg.body = contact_form.message.data
        mail.send(msg)
        return redirect(url_for('index')+'#contact')
    return render_template('index.html', form=contact_form)


@app.route('/portfolio', methods=["POST", "GET"])
def portfolio():
    morse_form = MorseForm()
    if morse_form.validate_on_submit():
        input_text = morse_form.input_field.data
        try:
            output_text = translate(input_text)
        except ValueError as error_message:
            output_text = str(error_message)
        return render_template('portfolio.html', form=morse_form, output=output_text)
    return render_template('portfolio.html', form=morse_form)


if __name__ == "__main__":
    app.run(debug=True)
