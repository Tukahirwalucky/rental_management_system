frappe.ui.form.on('Tenant', {
    refresh(frm) {
        frm.add_custom_button("View Statement", () => {
            frappe.call({
                method: "rental_management_system.api.view_tenant_statement",
                args: { tenant_id: frm.doc.name },
                callback: (r) => {
                    if (!r.exc) {
                        frappe.msgprint({
                            title: "Tenant Statement",
                            message: `<pre>${r.message}</pre>`,
                            indicator: "blue"
                        });
                    }
                }
            });
        });
    }
});
