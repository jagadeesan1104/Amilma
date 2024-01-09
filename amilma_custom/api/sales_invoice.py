import frappe

@frappe.whitelist()
def get_sales_id(db,outlet):
    status = ""
    try:
        get_sales_invoice = frappe.db.get_all("Sales Invoice", filters={'company':db,'customer':outlet,'status': ['not in', ['Paid']],'docstatus':1}, fields=['name'])
        status = True
    except Exception as e:
        status = False    
    return {"status":status,"sales_invoice":get_sales_invoice}