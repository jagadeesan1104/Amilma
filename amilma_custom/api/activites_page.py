import frappe
from frappe.utils import now,getdate,today,get_time,format_date,format_time



@frappe.whitelist()
def activites_data(user_id):
    message = ""
    get_in_time = ""
    get_out_time = ""
    lead_id = ""    
    lead_date = ""
    lead_time = ""
    customer_id = ""    
    customer_create_date = ""
    customer_create_time = ""
    purchase_order_id = ""
    purchase_created_date = ""
    purchase_created_time = ""
    sales_order_id = ""
    sales_created_date = ""
    sales_created_time = ""
    payment_entry_id = ""
    payment_entry_created_date = ""
    payment_entry_created_time = ""
    melting_claim_id = ""
    melting_claim_created_date = ""
    melting_claim_created_time = ""
    get_user_id = frappe.db.exists('User', {'name': user_id, 'enabled':1})
    if get_user_id:
        #global variables
        get_emp = frappe.db.get_value('Employee',{'user_id':get_user_id,'status':'Active'},['name'])
        if get_emp:
            #Employee Checkin data
            check_in_time = frappe.db.exists('Employee Checkin',{'employee':get_emp,'custom_punch_date':getdate(today()),'log_type':'IN'})
            if check_in_time:
                emp_checkin_in = frappe.get_doc('Employee Checkin',check_in_time)
                get_in_time = format_time(emp_checkin_in.time)
            else:
                get_in_time = ""    
            check_out_time = frappe.db.exists('Employee Checkin',{'employee':get_emp,'custom_punch_date':getdate(today()),'log_type':'OUT'})
            if check_out_time:
                emp_checkin_out = frappe.get_doc('Employee Checkin',check_out_time)
                get_out_time = format_time(emp_checkin_out.time)
            else:
                get_out_time = ""    
        else:
            message = "This User has no Employee ID"        
        
        #Lead Data
        check_lead = frappe.db.exists('Lead',{'owner':user_id})
        if check_lead:
            get_lead = frappe.get_doc('Lead',check_lead)
            if getdate(format_date(get_lead.creation)) == getdate(format_date(today())):
                lead_id = get_lead.name
                lead_date = getdate(format_date(get_lead.creation))
                lead_time = format_time(get_lead.creation)
            else:
                lead_id = ""    
                lead_date = ""
                lead_time = ""
        else:
            message = "Today No Lead  Created"      

        #Customer Data
        check_customer = frappe.db.exists('Customer',{'owner':user_id})    
        if check_customer:
            get_customer = frappe.get_doc('Customer',check_customer)
            if getdate(format_date(get_customer.creation)) == getdate(format_date(today())):
                customer_id = get_customer.name
                customer_create_date = getdate(format_date(get_customer.creation))
                customer_create_time = format_time(get_customer.creation)
            else:
                customer_id = ""    
                customer_create_date = ""
                customer_create_time = ""
        else:
            message = "Today No Customer  Created"       

        #purchase order data
        check_purchase_order = frappe.db.exists('Purchase Order',{'owner':user_id})
        if check_purchase_order:
            get_purchase_order = frappe.get_doc('Purchase Order',check_purchase_order)
            if getdate(format_date(get_purchase_order.creation)) == getdate(format_date(today())):
                purchase_order_id = get_purchase_order.name
                purchase_created_date = getdate(format_date(get_purchase_order.creation))
                purchase_created_time = format_time(get_purchase_order.creation)
            else:
                purchase_order_id = ""
                purchase_created_date = ""
                purchase_created_time = ""
        else:
            message = "Today No Purcchase Order  Created"  

        #sales order data
        check_sales_order = frappe.db.exists('Sales Order',{'owner':user_id})
        if check_sales_order:
            get_sales_order = frappe.get_doc('Sales Order',check_sales_order)
            if getdate(format_date(get_sales_order.creation)) == getdate(format_date(today())):
                sales_order_id = get_sales_order.name
                sales_created_date = getdate(format_date(get_sales_order.creation))
                sales_created_time = format_time(get_sales_order.creation)
            else:
                sales_order_id = ""
                sales_created_date = ""
                sales_created_time = ""
        else:
            message = "Today No Sales Order  Created"   

        #payment entry data
        check_payment_entry = frappe.db.exists('Payment Entry',{'owner':user_id})
        if check_payment_entry:
            get_payment_entry = frappe.get_doc('Payment Entry',check_payment_entry)
            if getdate(format_date(get_payment_entry.creation)) == getdate(format_date(today())):
                payment_entry_id = get_payment_entry.name
                payment_entry_created_date = getdate(format_date(get_payment_entry.creation))
                payment_entry_created_time = format_time(get_payment_entry.creation)
            else:
                payment_entry_id = ""
                payment_entry_created_date = ""
                payment_entry_created_time = ""
        else:
            message = "Today No Payment Entry  Created"   

        #melting claim data
        check_melting_claim = frappe.db.exists('Melting Claim',{'owner':user_id})
        if check_melting_claim:
            get_melting_claim = frappe.get_doc('Melting Claim',check_melting_claim)
            if getdate(format_date(get_melting_claim.creation)) == getdate(format_date(today())):
                melting_claim_id = get_melting_claim.name
                melting_claim_created_date = getdate(format_date(get_melting_claim.creation))
                melting_claim_created_time = format_time(get_melting_claim.creation)
            else:
                melting_claim_id = ""
                melting_claim_created_date = ""
                melting_claim_created_time = ""
        else:
            message = "Today No Metling Claim  Created"        

    else:
        message = "User have no ID" 

    #overall activites response    
    activites_data_page = {
        "punch_data_time":[
            {
                "punch_in":get_in_time,
                "punch_out":get_out_time 
            }
        ],
        "new_call_data":[
            {
                "lead_id":lead_id,
                "lead_creation":lead_date,
                "lead_time":lead_time,
            }
        ],
        "customer":[
            {
                "customer_id":customer_id,
                "customer_create_date":customer_create_date,
                "customer_create_time":customer_create_time
            }
        ],
        "purchase_order":[
            {
                "purchase_order_id": purchase_order_id,
                "purchase_created_date" : purchase_created_date,
                "purchase_created_time" : purchase_created_time
            }
        ],
        "sales_order":[
            {
                "sales_order_id":sales_order_id,
                "sales_created_date":sales_created_date,
                "sales_created_time":sales_created_time
            }
        ],
        "payment_entry":[
            {
                "payment_entry_id":payment_entry_id,
                "payment_entry_created_date":payment_entry_created_date,
                "payment_entry_created_time":payment_entry_created_time
            }
        ],
        "melting_claim":[
            {
                "melting_claim_id":melting_claim_id,
                "melting_claim_created_date":melting_claim_created_date,
                "melting_claim_created_time":melting_claim_created_time
            }
        ]
    }       
    return {"status":True,"message":message,"activites_page_data":activites_data_page}
