import frappe
from frappe.utils import now,getdate,today,format_date
from datetime import datetime
import json

# Create Claim
@frappe.whitelist()
def create_claim(user_id,db, outlet,melting_claim_items):
    convert_json = json.loads(melting_claim_items)
    status = ""
    try:
        get_user = frappe.db.exists('User',{'name':user_id,'enabled':1})
        if get_user:
            new_claim = frappe.new_doc('Melting Claim')
            new_claim.db = db
            new_claim.outlet = outlet
            for item in convert_json:
                new_claim.append("melting_claim_items",{
                    "item":item.get("item"),
                    'cate': item.get('cate'),
                    "req_qty":item.get("req_qty"),
                })
            new_claim.save(ignore_permissions=True)
            frappe.db.commit()
            frappe.db.set_value("Melting Claim",new_claim.name,"owner",user_id)
            status = True
            message = "New Claim Created"
        else:
            status = False
            message = "User has no ID or User ID Disabled"
        return {'status': status,'message': message}    
    except Exception as e:
        status = False
        return {"status": status, "message": e}

# melting claim list view
@frappe.whitelist()
def melting_claim_list(user_id):
    try:
        # Fetch Purchase Orders with items
        melting_claim_api = frappe.db.get_all('Melting Claim', {'owner': user_id},['*'])

        # Format the response
        formatted_melting_list = []
        for melting_claim in melting_claim_api:
            melting_claim_data = {
                'id':melting_claim.name,
                'name':melting_claim.name,
                'db_name': melting_claim.db,
                'outlet_name': melting_claim.outlet,
                'total_amount' :melting_claim.net_total,    
                'melting_claim_items': []
            }

            # Fetch items for each Purchase Order
            items = frappe.get_all('Melting Claim Items', filters={'parent': melting_claim.name},
                                   fields=['item', 'cate', 'req_qty', 'rate','amount'])

            for item in items:
                melting_claim_data['melting_claim_items'].append({
                    'item': item.item,
                    'cate': item.cate,
                    'req_qty': item.req_qty,
                    'rate': item.rate,
                    'amount':item.amount
                })

            formatted_melting_list.append(melting_claim_data)

        return {"status": True, "Item Details": formatted_melting_list}
    except:
        return {"status": False}

