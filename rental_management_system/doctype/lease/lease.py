import frappe

def on_submit(doc, method):
    create_invoice(doc)

def create_invoice(doc):
    frappe.get_doc({
        "doctype": "Invoice",
        "tenant": doc.tenant,
        "property": doc.property,
        "amount": doc.rent_amount,
        "due_date": doc.start_date,
        "status": "Unpaid"
    }).insert()

def validate(doc, method):
    if doc.end_date <= doc.start_date:
        frappe.throw("End date must be after start date.")
