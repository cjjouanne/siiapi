from src import app, bcrypt, db
from flask import render_template, flash, redirect, url_for, request
from ..forms.forms import ContactForm
from datetime import datetime
import sendgrid
from sendgrid.helpers.mail import *


@app.route('/contact', methods=['POST', 'GET'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        now = datetime.now()
        sg = sendgrid.SendGridAPIClient(api_key='sgApiKey')
        from_email = Email("notificadorelectrico@gmail.com")
        subject = "APISII"
        to_email = To('cjjouanne@uc.cl')
        content = Content("text/html", render_template('mailing/mail.html', sender=form.email.data, subject=form.subject.data, body=form.body.data, date=now))
        mail = Mail(from_email, to_email, subject, content)
        response = sg.client.mail.send.post(request_body=mail.get())
        form = ContactForm()
        return redirect(url_for('index'))
        
    return render_template('contact/index.html',form=form)
