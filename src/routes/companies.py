from src import app, bcrypt, db, login_manager
from flask_login import login_user, current_user, logout_user
from flask import jsonify, render_template, redirect, url_for, request
from ..models import User, Company
from ..forms.forms import CompanyForm
from datetime import datetime

@app.route('/empresas', methods=['POST', 'GET'])
def companies():
    if current_user.is_authenticated:
        form = CompanyForm()
        if form.validate_on_submit():
            now = datetime.now()
            apiKey = bcrypt.generate_password_hash(form.name.data+form.rut.data+str(now)).decode('utf-8')
            company = Company(name=form.name.data, rut=form.rut.data.replace('.',''), userId=current_user.id, apiKey=apiKey.replace('.','a').replace('/','z'))
            db.session.add(company)
            db.session.commit()
        companies=current_user.companies
        return render_template('companies/index.html',form=form, companies=companies, current_user=current_user)
    else:
        return redirect(url_for('index'))

@app.route('/deleteCompany', methods=['POST'])
def delete_company():
    if current_user.is_authenticated:
        company_id = request.form.get("company")
        company = Company.query.filter_by(id=int(company_id)).first()
        db.session.delete(company)
        db.session.commit()
        return redirect(url_for("companies"))
    else:
        redirect(url_for('index'))