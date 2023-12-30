import frappe
from frappe.utils import now,getdate,today,format_date,nowdate,add_months
from datetime import datetime


@frappe.whitelist()
def create_payment_entry(user_id,db,outlet,posting_date,mode_of_payment,paid_amount,transaction_reference_number,date,references):
    status = ""
    message = ""
    status = ""
    posting_date_format = datetime.strptime(format_date(posting_date), "%d-%m-%Y").date()
    # refrence_date = datetime.strptime(format_date(date), "%d-%m-%Y").date()
    try:
        payment_entry_references = frappe.parse_json(references)
        check_user_id = frappe.db.exists('User',{'name':user_id})
        if check_user_id:
            account_paid_to = get_payment_entry_account_paid_to(db)
            new_payment_entry = frappe.new_doc('Payment Entry')
            new_payment_entry.company = db
            new_payment_entry.posting_date = posting_date_format
            new_payment_entry.mode_of_payment = mode_of_payment
            new_payment_entry.payment_type = "Receive"
            new_payment_entry.party_type = "Customer"
            new_payment_entry.party = outlet
            new_payment_entry.paid_to = account_paid_to
            new_payment_entry.paid_amount = paid_amount
            new_payment_entry.received_amount = paid_amount
            for payment in payment_entry_references:
                new_payment_entry.append("references",{
                    "reference_doctype":payment.get("reference_doctype"),
                    "reference_name": payment.get("reference_name")
                })
            new_payment_entry.save(ignore_permissions=True)
            frappe.db.commit()

            status = True
            message = "New Payment Entry Created"
        else:
            status = False
        return {"status":status,"message":references}    
    except:
        status = False
        return{"status":status}    



def get_payment_entry_account_paid_to(company):
    get_account_paid_to = frappe.db.get_value('Account',{'company':company,'account_type':"Cash"},['name'])
    return get_account_paid_to


#payment entry list
@frappe.whitelist()
def payment_entry_list(user_id):
    try:
        payment_entry_list = frappe.get_all('Payment Entry', {'owner': user_id}, ['*'])

        formatted_payment_list = []
        for payment_entry in payment_entry_list:
            net_balance = payment_entry.difference_amount - payment_entry.total_allocated_amount
            payment_entry_data = {
                'id': payment_entry.name,
                'name': payment_entry.name,
                'select_db': payment_entry.company,
                'select_outlet': payment_entry.party,
                'select_date': payment_entry.posting_date,
                'paid_amount': payment_entry.paid_amount,
                'mode_of_payment': payment_entry.mode_of_payment,
                'date': payment_entry.posting_date,
                'transaction_reference_number': payment_entry.reference_no,
                'total_amount': payment_entry.paid_amount,
                'balance': payment_entry.difference_amount,
                'allocated': payment_entry.total_allocated_amount,
                'net_balance': net_balance,
                'references': []
            }
            references = frappe.get_all('Payment Entry Reference', {'parent': payment_entry.name}, ['*'])
            for item in references:
                payment_entry_data['references'].append({
                    'invoice_no': item.reference_name,
                    'invoice_date': item.due_date,
                    'amount': item.allocated_amount,
                    'balance': item.outstanding_amount
                })
            formatted_payment_list.append(payment_entry_data)

        return {"status": True, "Payment_Entry": formatted_payment_list}
    except:
        return {"status": False}

#sales outlet details
@frappe.whitelist()
def sales_outlet_details(user_id,company,outlet):
    status = ""
    try:
        check_user_id = frappe.db.exists("User",{'name':user_id})
        if check_user_id:
            customer = frappe.db.get_value('Customer',{'name':outlet},['customer_name','territory'])
            freezer_data = frappe.db.get_value('Freezer Data',{'dealer':outlet},['make','model','capacity','basket','serial_no'])
            current_month_sales_amount = outlet_current_month_sales(outlet,user_id,company)
            third_month_sales_amount = outlet_third_month_sales(outlet,user_id,company) or 0
            second_month_sales_amount = outlet_second_month_sales(outlet,user_id,company) or 0
            first_month_sales_amount = outlet_first_month_sales(outlet,user_id,company) or 0
            outlet_details_list = {
                "outlte_name":customer[0],
                "status":"Active",
                "route":customer[1],
                "current_month_sales":current_month_sales_amount,
                "third_month_sales_amount":third_month_sales_amount,
                "second_month_sales_amount":second_month_sales_amount,
                "first_month_sales_amount":first_month_sales_amount,
                "freezer_make_and_model":f"{freezer_data[0]}|{freezer_data[1]}",
                "freezer_capacity":freezer_data[2],
                "no_of_baskets":freezer_data[3],
                "freezer_serial_number":freezer_data[4]
            }
            status = True
        else:
            status = False  
        return {"status":status,"outlet_details_list":outlet_details_list}    
    except:
        status = False
        return{"status":status}  

#current month sales order get the rounded total amount and sum it       
def outlet_current_month_sales(outlet,user_id,company):
    current_month_sales_amount = 0.0
    today = nowdate()
    month_start_date = frappe.utils.data.get_first_day(today)
    month_end_date = frappe.utils.data.get_last_day(today)
    get_sales_amount = frappe.db.sql(""" select sum(rounded_total) as net_total from `tabSales Order` where company = '%s' and customer = '%s' and owner = '%s' and transaction_date between '%s' and '%s' and docstatus = 1 """%(company,outlet,user_id,month_start_date,month_end_date),as_dict=1) or 0
    if get_sales_amount:
        current_month_sales_amount = get_sales_amount[0]['net_total']
    else:
        current_month_sales_amount = 0.0
    return current_month_sales_amount

#third month sales order get the rounded total amount and sum it    
def outlet_third_month_sales(outlet,user_id,company):
    third_month_sales_amount = 0
    current_date = nowdate()

    third_month_start_date = frappe.utils.data.get_first_day(current_date)

    get_third_month_start_date = add_months(third_month_start_date,-1)
    get_third_month_end_date = frappe.utils.data.get_last_day(get_third_month_start_date)
    
    get_sales_amount = frappe.db.sql(""" select sum(rounded_total) as net_total from `tabSales Order` where company = '%s' and customer = '%s' and owner = '%s' and transaction_date between '%s' and '%s' and docstatus = 1 """ % (company, outlet, user_id, get_third_month_start_date, get_third_month_end_date), as_dict=1)
    third_month_sales_amount = get_sales_amount[0]['net_total'] if get_sales_amount and get_sales_amount[0]['net_total'] is not None else 0
    return third_month_sales_amount

#second month sales order get the rounded total amount and sum it 
def outlet_second_month_sales(outlet,user_id,company):
    second_month_sales_amount = 0.0
    current_date = nowdate()

    second_month_start_date = frappe.utils.data.get_first_day(current_date)

    get_second_month_start_date = add_months(second_month_start_date,-2)
    get_second_month_end_date = frappe.utils.data.get_last_day(get_second_month_start_date)
    
    get_sales_amount = frappe.db.sql(""" select sum(rounded_total) as net_total from `tabSales Order` where company = '%s' and customer = '%s' and owner = '%s' and transaction_date between '%s' and '%s' and docstatus = 1 """ % (company, outlet, user_id, get_second_month_start_date, get_second_month_end_date), as_dict=1)
    second_month_sales_amount = get_sales_amount[0]['net_total'] if get_sales_amount and get_sales_amount[0]['net_total'] is not None else 0
    return second_month_sales_amount

#first month sales order get the rounded total amount and sum it 
def outlet_first_month_sales(outlet,user_id,company):
    first_month_sales_amount = 0.0
    current_date = nowdate()

    first_month_start_date = frappe.utils.data.get_first_day(current_date)

    get_first_month_start_date = add_months(first_month_start_date,-3)
    get_first_month_end_date = frappe.utils.data.get_last_day(get_first_month_start_date)
    
    get_sales_amount = frappe.db.sql(""" select sum(rounded_total) as net_total from `tabSales Order` where company = '%s' and customer = '%s' and owner = '%s' and transaction_date between '%s' and '%s' and docstatus = 1 """ % (company, outlet, user_id, get_first_month_start_date, get_first_month_end_date), as_dict=1)
    first_month_sales_amount = get_sales_amount[0]['net_total'] if get_sales_amount and get_sales_amount[0]['net_total'] is not None else 0
    return first_month_sales_amount

@frappe.whitelist()
def get_payment_entry_invoice_data(user_id,company,outlet):
    status = ""
    try:
        check_user_id = frappe.db.exists("User",{'name':user_id})
        if check_user_id:
            get_sales_invoice = frappe.db.get_all("Sales Invoice",{'owner':user_id,'company':company,'customer':outlet},['name','posting_date','rounded_total','outstanding_amount'])
            status = True
        else:
            status = False
        return{"status":status,"type_of_payment_entry":get_sales_invoice}    
    except:
        status = False
        return{"status":status}