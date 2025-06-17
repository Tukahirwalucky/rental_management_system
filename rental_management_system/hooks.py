app_name = "rental_management_system"
app_title = "Rental Management System"
app_publisher = "Emily"
app_description = "Managing tenants"
app_email = "emilylucky062@gmail.com"
app_license = "MIT"

# Include JavaScript files
app_include_js = [
    "/assets/rental_management_system/js/rental_management_system.js",
    "/assets/rental_management_system/js/lease.js",
    "/assets/rental_management_system/js/invoice.js",
    "/assets/rental_management_system/js/property_list.js",
    "/assets/rental_management_system/js/tenant.js"
]

# Fixtures for exporting custom DocTypes and related customizations
fixtures = [
    {
        "doctype": "DocType",
        "filters": [
            ["name", "in", [
                "Tenant",
                "Property",
                "Lease",
                "Invoice",
                "Rental Settings",
                "Payments"
            ]]
        ]
    },
    {
        "doctype": "Custom Field",
        "filters": [
            ["dt", "in", [
                "Tenant",
                "Property",
                "Lease",
                "Invoice",
                "Rental Settings",
                "Payments"
            ]]
        ]
    },
    {
        "doctype": "Property Setter"
    },
    {
        "doctype": "Client Script"
    },
    {
        "doctype": "Server Script"
    }
]

# Document Events
doc_events = {
    "Lease": {
        "on_submit": "rental_management_system.doctype.lease.lease.on_submit",
        "validate": "rental_management_system.doctype.lease.lease.validate"
    }
}

# Scheduled Tasks
scheduler_events = {
    "daily": [
        "rental_management_system.api.send_due_rent_emails"
    ],
    "cron": {
        "0 0 28-31 * *": [
            "rental_management_system.api.generate_month_end_invoices"
        ]
    }
}
