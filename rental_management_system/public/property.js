frappe.listview_settings['Property'] = {
    onload(listview) {
        listview.page.add_menu_item('Mark as Vacant', () => {
            let selected = listview.get_checked_items();
            if (selected.length === 0) {
                frappe.msgprint("Please select properties to mark as vacant.");
                return;
            }

            let names = selected.map(item => item.name);

            frappe.call({
                method: "rental_management_system.api.mark_properties_vacant",
                args: { property_names: names },
                callback: () => {
                    frappe.msgprint("Selected properties marked as vacant.");
                    listview.refresh();
                }
            });
        });
    }
};
