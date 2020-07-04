from flask import Blueprint, render_template, request, flash
from flask_login import current_user, login_required
account_bp = Blueprint('account_bp',__name__,template_folder='templates')
from application.db_invoice import getAllInvoices, liveSearchInvoices, updateSubmitted, updateCredit, getInvoiceByInvoiceName
import simplejson as json
from datetime import datetime
import datetime as datetime2

@account_bp.route("/", methods=['GET','POST'])
@login_required 
def gerneral():
    invoices = getAllInvoices(current_user.uuid)
    for i in invoices:
        for o in i:
            if isinstance(i[o], datetime2.datetime):
                d = datetime.strptime(i[o].__str__(), '%Y-%m-%d %H:%M:%S')
                date = d.strftime('%d.%m.%Y')
                i[o] = date
    return render_template('account_bp/general.html',
            invoices = json.dumps(invoices))


@account_bp.route("/invoices-due", methods=['GET'])
@login_required 
def due():
    return render_template('account_bp/due.html')


@account_bp.route("/invoices-not-submitted", methods=['GET'])
@login_required 
def unsubmitted():
    return render_template('account_bp/not_submitted.html')


@account_bp.route("/settings", methods=['GET'])
@login_required 
def settings():
    return render_template('account_bp/settings.html')


@account_bp.route("/invoice/<medical>/<year>/<index>", methods=['GET'])
@login_required 
def singleInvoice(medical, year, index):
    invoice_name = medical + "/" + year + "/" + index
    print(invoice_name)
    invoice = getInvoiceByInvoiceName(current_user.uuid, invoice_name)
    for o, i in invoice.items():
         if isinstance(i, datetime2.datetime):
             d = datetime.strptime(i.__str__(), '%Y-%m-%d %H:%M:%S')
             date = d.strftime('%d.%m.%Y')
             invoice[o] = date
    return render_template('account_bp/invoice.html',
            invoice_json = json.dumps(invoice),
            invoice = invoice)


@account_bp.route('/live-search-invoice',methods=['GET','POST'])
@login_required
def liveSearchTreatment():
    name = request.args.get('name')
    invoices = liveSearchInvoices(current_user.uuid, name)
    for i in invoices:
        for o in i:
            if isinstance(i[o], datetime2.datetime):
                d = datetime.strptime(i[o].__str__(), '%Y-%m-%d %H:%M:%S')
                date = d.strftime('%d.%m.%Y')
                i[o] = date
    return json.dumps({'invoices' : invoices})

@account_bp.route('/submit-invoice',methods=['GET'])
def submitInvoice():
    invoice_name = request.args.get('invoice_name')
    status = updateSubmitted(current_user.uuid, invoice_name)
    if status:
        return json.dumps(invoice_name + " was succesfully submitted")
    else:
        return json.dumps("Something went wrong. Please contact the system administrator")


@account_bp.route('/add-credit-invoice',methods=['GET'])
def addCreditInvoice():
    invoice_name = request.args.get('invoice_name')
    credit = request.args.get('credit')
    status = updateDebit(current_user.uuid, invoice_name, credit)
    if status:
        return json.dumps(invoice_name + " marked as paid")
    else:
        return json.dumps('Could not add debit to invoice account. Please contact the system administator')
