import frappe
from datetime import datetime
from dateutil.relativedelta import relativedelta
from frappe.utils import nowdate, add_months

@frappe.whitelist()
def get_pending_amount():
    result = frappe.db.sql("""
        SELECT SUM(outstanding_amount) 
        FROM `tabSales Invoice` 
        WHERE docstatus = 1 AND status = 'Unpaid'
    """, as_dict=True)
    return result[0]['SUM(outstanding_amount)'] or 0

@frappe.whitelist()
def get_properties_counts():
    total = frappe.db.count('Property')
    active = frappe.db.count('Property', {'status': 'Active'})
    return {'total': total, 'active': active}

@frappe.whitelist()
def get_monthly_payments():
    today = datetime.today()
    start_date = (today - relativedelta(months=11)).replace(day=1)
    payments = frappe.db.sql("""
        SELECT 
            DATE_FORMAT(posting_date, '%%Y-%%m') as month, 
            SUM(base_amount) as amount
        FROM `tabPayment Entry`
        WHERE docstatus = 1 AND posting_date >= %s
        GROUP BY month
        ORDER BY month
    """, start_date, as_dict=True)

    payment_map = {p['month']: p['amount'] for p in payments}

    month_labels = []
    amounts = []

    for i in range(12):
        month = (start_date + relativedelta(months=i)).strftime('%Y-%m')
        month_labels.append(month)
        amounts.append(payment_map.get(month, 0))

    return {
        'labels': month_labels,
        'datasets': [{
            'name': 'Monthly Payments',
            'values': amounts
        }]
    }

# ---------- Automation Scripts ----------

def generate_month_end_invoices():
    leases = frappe.get_all("Lease", filters={"status": "Active"})
    for lease in leases:
        lease_doc = frappe.get_doc("Lease", lease.name)
        frappe.get_doc({
            "doctype": "Invoice",
            "tenant": lease_doc.tenant,
            "property": lease_doc.property,
            "amount": lease_doc.rent_amount,
            "due_date": add_months(lease_doc.start_date, 1),
            "status": "Unpaid"
        }).insert()

def send_due_rent_emails():
    invoices = frappe.get_all("Invoice", filters={"status": "Unpaid"})
    for inv in invoices:
        doc = frappe.get_doc("Invoice", inv.name)
        if nowdate() > doc.due_date:
            tenant_email = frappe.db.get_value("Tenant", doc.tenant, "email")
            if tenant_email:
                frappe.sendmail(
                    recipients=[tenant_email],
                    subject="Rent Due Reminder",
                    message=f"Dear Tenant, your rent for property {doc.property} is overdue. Please pay immediately."
                )
