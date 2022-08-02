from src import app, bcrypt, db
from flask import render_template, flash, redirect, url_for, request
from ..forms.forms import ContactForm
from datetime import datetime


@app.route('/docs', methods=['GET'])
def docs():
    origin = 'https://siiapi.ga'
    return render_template('docs/index.html', origin=origin)