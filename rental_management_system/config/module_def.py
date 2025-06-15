from frappe import _

def get_data():
    return {
        "fieldname": "rental_management",
        "transactions": [
            {
                "label": _("Rental Management"),
                "items": ["Tenant", "Property", "Lease", "Invoice", "Payment", "Rental Settings"]
            }
        ]
    }
