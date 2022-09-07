from flask import Flask, render_template, send_from_directory
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, EmailField
from wtforms.validators import DataRequired, Email
import smtplib
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")

bootstrap = Bootstrap(app)
EMAIL = os.environ.get("EMAIL")
PASS = os.environ.get("PASS")



class ContactForm(FlaskForm):
    name = StringField("Name:", validators=[DataRequired()])
    email = EmailField("Email:", validators=[DataRequired(), Email()])
    message = TextAreaField("Message:", validators=[DataRequired()])
    submit = SubmitField("Send")


@app.route('/', methods=["GET", "POST"])
def index():
    form = ContactForm()
    if form.validate_on_submit():
        with smtplib.SMTP("smtp.gmail.com", 587) as connection:
            connection.starttls()
            connection.login(user=EMAIL, password=PASS)
            connection.sendmail(from_addr=EMAIL, to_addrs=EMAIL, msg=f"Subject: New message from: {form.name.data}\n\n"
                                                                     f"E-mail: {form.email.data}\n"
                                                                     f"{form.message.data}")
            form.name.data = ""
            form.email.data = ""
            form.message.data = ""
    return render_template("index.html", form=form)

@app.route('/download')
def download():
    return send_from_directory(
        directory="static/files",
        path="resume_Adelin_Gruian.pdf"
    )


if __name__ == '__main__':
    app.run(debug=True)
