import requests
import json
from src import app, bcrypt, db
from flask import render_template, flash, redirect, url_for, request
from ..models import User, Company
from datetime import datetime

doc_types = [
    { 'name': 'Factura', 'value': '30' },
    { 'name': 'Factura Excenta', 'value': '32' },
    { 'name': 'Factura Electronica', 'value': '33' },
    { 'name': 'Factura Electronica Excenta', 'value': '34' },
    { 'name': 'Boleta', 'value': '35' },
    { 'name': 'Boleta Excenta', 'value': '38' },
    { 'name': 'Boleta Electronica', 'value': '39' },
    { 'name': 'Liquidación-Factura', 'value': '40' },
    { 'name': 'Boleta Electronica Excenta', 'value': '41' },
    { 'name': 'Liquidación-Factura Electronica', 'value': '43' },
    { 'name': 'Factura de Compra', 'value': '45' },
    { 'name': 'Factura Electronica de Compra', 'value': '46' },
    { 'name': 'Guia de Despacho', 'value': '50' },
    { 'name': 'Guia de Despacho Electronica', 'value': '52' },
    { 'name': 'Nota de Debito', 'value': '55' },
    { 'name': 'Nota de Debito Electronica', 'value': '56' },
    { 'name': 'Nota de Credito', 'value': '60' },
    { 'name': 'Nota de Credito Electronica', 'value': '61' },
    { 'name': 'Liquidacion', 'value': '103' },
    { 'name': 'Factura de Exportacion Electronica', 'value': '110' },
    { 'name': 'Nota de Debito de Exportacion Electronica', 'value': '111' },
    { 'name': 'Nota de Credito de Exportacion Electronica', 'value': '112' },
]

# bt_ingresar
def getCookies(cookie_jar, domain):
    cookie_dict = cookie_jar.get_dict()
    found = ['%s=%s' % (name, value) for (name, value) in cookie_dict.items()]
    return ';'.join(found), cookie_dict['TOKEN']

def sii_login(rut, clave):
    LOGIN = 'https://zeusr.sii.cl/cgi_AUT2000/CAutInicio.cgi'
    payload = {
        'rut': rut[:-2].replace('.', ''),
        'dv': rut[-1],
        'referencia': 'https://www.sii.cl',
        'rutcntr': rut,
        'clave': clave,
        'bt_ingresar': 'bt_ingresar',
    }
    req = requests.Session()
    req.post(LOGIN, data=payload)
    cookies, token = getCookies(req.cookies, 'www.sii.cl')
    headers = {
        'Content-type': 'application/json',
        'Pragma': 'no-cache',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'es-419,es;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Cache-Control': 'no-cache',
        'Content-Length': '341',
        'Referer': 'https://www4.sii.cl/consdcvinternetui/',
        'Host': 'www4.sii.cl',
        'Cookie': cookies,
    }
    return token, headers

@app.route('/api/v1/getDocumentTypes', methods=['GET'])
def get_document_types():
    return json.dumps(doc_types)


@app.route('/api/v1/getResumen/compra/<apiKey>/<rut>/<password>/<period>', methods=['GET'])
def get_resumen_compra(apiKey, rut, password, period):
    user = User.query.filter_by(apiKey=apiKey).first()
    if user:
        if rut.replace('.', '') in user.get_company_ruts():
            req = requests.Session()
            token, headers = sii_login(rut, password)
            data = { "metaData": { "namespace": "cl.sii.sdi.lob.diii.consdcv.data.api.interfaces.FacadeService/getResumen", "conversationId": token, "transactionId": "1", "page": None }, "data": { "rutEmisor": rut[:-2].replace('.', ''), "dvEmisor": rut[-1], "ptributario": period, "estadoContab": "REGISTRO", "operacion": "COMPRA", "busquedaInicial": True } }
            r2 = req.post('https://www4.sii.cl/consdcvinternetui/services/data/facadeService/getResumen', headers=headers, data=json.dumps(data))
            return parseResumen(r2.content)
    return '401'

@app.route('/api/v1/getDetalle/compra/<apiKey>/<rut>/<password>/<doc_type>/<period>', methods=['GET'])
def get_detalle_compra_documento(apiKey, rut, password, doc_type, period):
    user = User.query.filter_by(apiKey=apiKey).first()
    if user:
        if rut.replace('.', '') in user.get_company_ruts():
            req = requests.Session()
            token, headers = sii_login(rut, password)
            data = { "metaData": { "namespace": "cl.sii.sdi.lob.diii.consdcv.data.api.interfaces.FacadeService/getDetalleCompra", "conversationId": token,"transactionId":"1", "page": None }, "data": { "rutEmisor": rut[:-2].replace('.', ''), "dvEmisor": rut[-1], "ptributario": period, "codTipoDoc": doc_type, "operacion": "COMPRA", "estadoContab": "REGISTRO" } }
            r2 = req.post('https://www4.sii.cl/consdcvinternetui/services/data/facadeService/getDetalleCompra', headers=headers, data=json.dumps(data))
            return parseResumen(r2.content)
    return '401'

@app.route('/api/v1/getDetalleExport/compra/<apiKey>/<rut>/<password>/<period>', methods=['GET'])
def detalleCompraExport(apiKey, rut, password, period):
    user = User.query.filter_by(apiKey=apiKey).first()
    if user:
        if rut.replace('.', '') in user.get_company_ruts():
            req = requests.Session()
            token, headers = sii_login(rut, password)
            data = { "metaData": { "namespace": "cl.sii.sdi.lob.diii.consdcv.data.api.interfaces.FacadeService/getDetalleCompraExport", "conversationId": token, "transactionId": "1","page": None }, "data": { "rutEmisor": rut[:-2].replace('.', ''), "dvEmisor": rut[-1], "ptributario": period, "codTipoDoc": 0, "operacion": "COMPRA", "estadoContab": "REGISTRO" } }
            r2 = req.post('https://www4.sii.cl/consdcvinternetui/services/data/facadeService/getDetalleCompraExport', headers=headers, data=json.dumps(data))
            return json.dumps(parseDetalleExport(r2.content))
    return '401'

@app.route('/api/v1/getResumen/venta/<apiKey>/<rut>/<password>/<period>', methods=['GET'])
def get_resumen_venta(apiKey, rut, password, period):
    user = User.query.filter_by(apiKey=apiKey).first()
    if user:
        if rut.replace('.', '') in user.get_company_ruts():
            req = requests.Session()
            token, headers = sii_login(rut, password)
            data = { "metaData": { "namespace": "cl.sii.sdi.lob.diii.consdcv.data.api.interfaces.FacadeService/getResumen", "conversationId": token, "transactionId": "1", "page": None }, "data": { "rutEmisor": rut[:-2].replace('.', ''), "dvEmisor": rut[-1], "ptributario": period, "estadoContab": "REGISTRO", "operacion": "VENTA", "busquedaInicial": True } }
            r2 = req.post('https://www4.sii.cl/consdcvinternetui/services/data/facadeService/getResumen', headers=headers, data=json.dumps(data))
            return parseResumen(r2.content)
    return '401'

@app.route('/api/v1/getDetalle/venta/<apiKey>/<rut>/<password>/<doc_type>/<period>', methods=['GET'])
def get_detalle_venta_documento(apiKey, rut, password, doc_type, period):
    user = User.query.filter_by(apiKey=apiKey).first()
    if user:
        if rut.replace('.', '') in user.get_company_ruts():
            req = requests.Session()
            token, headers = sii_login(rut, password)
            data = { "metaData": { "namespace": "cl.sii.sdi.lob.diii.consdcv.data.api.interfaces.FacadeService/getDetalleVenta", "conversationId": token,"transactionId":"1", "page": None }, "data": { "rutEmisor": rut[:-2].replace('.', ''), "dvEmisor": rut[-1], "ptributario": period, "codTipoDoc": doc_type, "operacion": "VENTA", "estadoContab": "REGISTRO" } }
            r2 = req.post('https://www4.sii.cl/consdcvinternetui/services/data/facadeService/getDetalleVenta', headers=headers, data=json.dumps(data))
            return parseResumen(r2.content)
    return '401'

@app.route('/api/v1/getDetalleExport/venta/<apiKey>/<rut>/<password>/<period>', methods=['GET'])
def detalleVentaExport(apiKey, rut, password, period):
    user = User.query.filter_by(apiKey=apiKey).first()
    if user:
        if rut.replace('.', '') in user.get_company_ruts():
            req = requests.Session()
            token, headers = sii_login(rut, password)
            data = { "metaData": { "namespace": "cl.sii.sdi.lob.diii.consdcv.data.api.interfaces.FacadeService/getDetalleVentaExport", "conversationId": token, "transactionId":"1", "page": None }, "data": { "rutEmisor": rut[:-2].replace('.', ''), "dvEmisor": rut[-1], "ptributario": period, "codTipoDoc": 0, "operacion": "VENTA", "estadoContab": "" }}
            r2 = req.post('https://www4.sii.cl/consdcvinternetui/services/data/facadeService/getDetalleVentaExport', headers=headers, data=json.dumps(data))
            return json.dumps(parseDetalleExport(r2.content))
    return '401'




#_______________________________________________________________________________________________________

@app.route('/api/v1/company/getResumen/compra/<apiKey>/<password>/<period>', methods=['GET'])
def company_get_resumen_compra(apiKey, password, period):
    company = Company.query.filter_by(apiKey=apiKey).first()
    if company:
        rut = company.rut
        req = requests.Session()
        token, headers = sii_login(rut, password)
        data = { "metaData": { "namespace": "cl.sii.sdi.lob.diii.consdcv.data.api.interfaces.FacadeService/getResumen", "conversationId": token, "transactionId": "1", "page": None }, "data": { "rutEmisor": rut[:-2].replace('.', ''), "dvEmisor": rut[-1], "ptributario": period, "estadoContab": "REGISTRO", "operacion": "COMPRA", "busquedaInicial": True } }
        r2 = req.post('https://www4.sii.cl/consdcvinternetui/services/data/facadeService/getResumen', headers=headers, data=json.dumps(data))
        return parseResumen(r2.content)
    return '401'

@app.route('/api/v1/company/getDetalle/compra/<apiKey>/<password>/<doc_type>/<period>', methods=['GET'])
def company_get_detalle_compra_documento(apiKey, password, doc_type, period):
    company = Company.query.filter_by(apiKey=apiKey).first()
    if company:
        rut = company.rut
        req = requests.Session()
        token, headers = sii_login(rut, password)
        data = { "metaData": { "namespace": "cl.sii.sdi.lob.diii.consdcv.data.api.interfaces.FacadeService/getDetalleCompra", "conversationId": token,"transactionId":"1", "page": None }, "data": { "rutEmisor": rut[:-2].replace('.', ''), "dvEmisor": rut[-1], "ptributario": period, "codTipoDoc": doc_type, "operacion": "COMPRA", "estadoContab": "REGISTRO" } }
        r2 = req.post('https://www4.sii.cl/consdcvinternetui/services/data/facadeService/getDetalleCompra', headers=headers, data=json.dumps(data))
        return parseResumen(r2.content)
    return '401'

@app.route('/api/v1/company/getDetalleExport/compra/<apiKey>/<password>/<period>', methods=['GET'])
def companyDetalleCompraExport(apiKey, password, period):
    company = Company.query.filter_by(apiKey=apiKey).first()
    if company:
        rut = company.rut
        req = requests.Session()
        token, headers = sii_login(rut, password)
        data = { "metaData": { "namespace": "cl.sii.sdi.lob.diii.consdcv.data.api.interfaces.FacadeService/getDetalleCompraExport", "conversationId": token, "transactionId": "1","page": None }, "data": { "rutEmisor": rut[:-2].replace('.', ''), "dvEmisor": rut[-1], "ptributario": period, "codTipoDoc": 0, "operacion": "COMPRA", "estadoContab": "REGISTRO" } }
        r2 = req.post('https://www4.sii.cl/consdcvinternetui/services/data/facadeService/getDetalleCompraExport', headers=headers, data=json.dumps(data))
        return json.dumps(parseDetalleExport(r2.content))
    return '401'

@app.route('/api/v1/company/getResumen/venta/<apiKey>/<password>/<period>', methods=['GET'])
def company_get_resumen_venta(apiKey, password, period):
    company = Company.query.filter_by(apiKey=apiKey).first()
    if company:
        rut = company.rut
        req = requests.Session()
        token, headers = sii_login(rut, password)
        data = { "metaData": { "namespace": "cl.sii.sdi.lob.diii.consdcv.data.api.interfaces.FacadeService/getResumen", "conversationId": token, "transactionId": "1", "page": None }, "data": { "rutEmisor": rut[:-2].replace('.', ''), "dvEmisor": rut[-1], "ptributario": period, "estadoContab": "REGISTRO", "operacion": "VENTA", "busquedaInicial": True } }
        r2 = req.post('https://www4.sii.cl/consdcvinternetui/services/data/facadeService/getResumen', headers=headers, data=json.dumps(data))
        return parseResumen(r2.content)
    return '401'

@app.route('/api/v1/company/getDetalle/venta/<apiKey>/<password>/<doc_type>/<period>', methods=['GET'])
def company_get_detalle_venta_documento(apiKey, password, doc_type, period):
    company = Company.query.filter_by(apiKey=apiKey).first()
    if company:
        rut = company.rut
        req = requests.Session()
        token, headers = sii_login(rut, password)
        data = { "metaData": { "namespace": "cl.sii.sdi.lob.diii.consdcv.data.api.interfaces.FacadeService/getDetalleVenta", "conversationId": token,"transactionId":"1", "page": None }, "data": { "rutEmisor": rut[:-2].replace('.', ''), "dvEmisor": rut[-1], "ptributario": period, "codTipoDoc": doc_type, "operacion": "VENTA", "estadoContab": "REGISTRO" } }
        r2 = req.post('https://www4.sii.cl/consdcvinternetui/services/data/facadeService/getDetalleVenta', headers=headers, data=json.dumps(data))
        return parseResumen(r2.content)
    return '401'

@app.route('/api/v1/company/getDetalleExport/venta/<apiKey>/<password>/<period>', methods=['GET'])
def companyDetalleVentaExport(apiKey, password, period):
    company = Company.query.filter_by(apiKey=apiKey).first()
    if company:
        rut = company.rut
        req = requests.Session()
        token, headers = sii_login(rut, password)
        data = { "metaData": { "namespace": "cl.sii.sdi.lob.diii.consdcv.data.api.interfaces.FacadeService/getDetalleVentaExport", "conversationId": token, "transactionId":"1", "page": None }, "data": { "rutEmisor": rut[:-2].replace('.', ''), "dvEmisor": rut[-1], "ptributario": period, "codTipoDoc": 0, "operacion": "VENTA", "estadoContab": "" }}
        r2 = req.post('https://www4.sii.cl/consdcvinternetui/services/data/facadeService/getDetalleVentaExport', headers=headers, data=json.dumps(data))
        return json.dumps(parseDetalleExport(r2.content))
    return '401'

def parseDetalleExport(data):
    data_dict = json.loads(data.decode('utf8').replace("'", '"'))
    data_list = data_dict['data'][1:]
    data_headers = data_dict['data'][0].split(';')
    new_data = []
    for i in data_list:
        new_dict = {}
        i_list = i.split(';')
        for j in range(len(i_list)-1):
            new_dict[data_headers[j]]=i_list[j]
        new_data.append(new_dict)
    data_dict['data']=new_data
    return data_dict

def parseResumen(data):
    return data.decode('utf8').replace("'", '"')