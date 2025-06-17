frappe.ui.form.on('Invoice', {
    refresh(frm) {
        // Add "Send Reminder" button if unpaid
        if (frm.doc.docstatus === 1 && frm.doc.status === "Unpaid") {
            frm.add_custom_button("Send Reminder", () => {
                frappe.call({
                    method: "rental_management_system.api.send_rent_reminder",
                    args: { invoice_name: frm.doc.name },
                    callback: (r) => {
                        if (!r.exc) {
                            frappe.msgprint("Reminder email sent to tenant.");
                        }
                    }
                });
            });
        }
    },

    status(frm) {
        // Hide due_date if paid
        if (frm.doc.status === "Paid") {
            frm.set_df_property("due_date", "hidden", true);
        } else {
            frm.set_df_property("due_date", "hidden", false);
        }
    }
});
