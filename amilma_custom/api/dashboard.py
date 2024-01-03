import frappe
from frappe.utils import now,getdate,today,nowdate
from datetime import datetime


#the below code is for APK Dashboard activites page list the number of datas
@frappe.whitelist()
def dashboard_activites(user_id):
    status = ""
    user_name = frappe.db.get_value('Employee',{'status':'Active','user_id':user_id},['user_id'])
    if user_name:
        get_emp_id = frappe.db.get_value('Employee',{'status':'Active','user_id':user_id},['name'])
        get_emp_checkin =  frappe.db.get_value('Employee Checkin',{'employee':get_emp_id,'custom_punch_date':getdate(today())},['log_type'])
        if get_emp_checkin:
            get_log_type = get_emp_checkin
        else:
            get_log_type = ""    
        status = True
    else:
        status = False
    dashboard = {
        "activites":[
            {
                "description": "Monthly Target",
                "key":1,
                "primary": "12",
                "secondary": "20"
            },
             {
                "description": "Monthly Achieved",
                "key":2,
                "primary": "12",
                "secondary": "20"
            },
             {
                "description": "Total Achieved",
                "key":3,
                "primary": "12",
                "secondary": "20"
            }
        ],
        "your_works":[
            {
                "description": "New Calls",
                "key":3,
                "overall":"12",
                "route":"15"
            },
            {
                "description": "Outlet",
                "key":4,
                "overall":"12",
                "route":"15"
            },
            {
                "description": "Conversion",
                "key":5,
                "overall":"12",
                "route":"15"
            },
            {
                "description": "Active",
                "key":6,
                "overall":"12",
                "route":"15"
            },
            {
                "description": "Inactive",
                "key":7,
                "overall":"12",
                "route":"15"
            },
            {
                "description": "Pullout",
                "key":8,
                "overall":"12",
                "route":"15"
            },
            {
                "description": "Complaint",
                "key":9,
                "overall":"12",
                "route":"15"
            },
            {
                "description": "DB Point",
                "key":10,
                "overall":"12",
                "route":"15"
            }
        ],
        "log_type":get_log_type
    }
    return{'status':status,'message':'Succesfully','Dashboard':dashboard}

def get_monthly_target_as_primary(user_id):
    today = nowdate()
    get_primary_monthly_target = ""
    try:
        start_date = datetime.strptime(today, '%Y-%m-%d').month
        check_user_id = frappe.db.exists("User",{'name':user_id})
        if check_user_id:
            emp_in_user_id = frappe.db.exists("Employee",{'status':'Active','user_id':user_id})
            if emp_in_user_id:
                get_emp = frappe.db.get_value('Employee',{'name':emp_in_user_id},['designation'])
                if get_emp == "Sales Officer":
                    get_primary_monthly_target = frappe.db.sql(""" select sum(target_amount) as target_amount from `tabAmilma Target Setting` where month = '%s' and so_designation = "Sales Officer"  and type = "Primary" """%(start_date),as_dict=1)
                elif get_emp == "Area Sales Manager":
                    get_primary_monthly_target = frappe.db.sql(""" select sum(target_amount) as target_amount from `tabAmilma Target Setting` where month = '%s' and so_designation = "Area Sales Manager"  and type = "Primary" """%(start_date),as_dict=1)
                elif get_emp == "Regional Sales Manager":
                    get_primary_monthly_target = frappe.db.sql(""" select sum(target_amount) as target_amount from `tabAmilma Target Setting` where month = '%s' and so_designation = "Regional Sales Manager"  and type = "Primary" """%(start_date),as_dict=1)
                else:
                    get_primary_monthly_target = ""
        return get_primary_monthly_target     
    except:
        return get_primary_monthly_target


def get_monthly_target_as_secondary(user_id):
    today = nowdate()
    get_primary_monthly_target = ""
    try:
        start_date = datetime.strptime(today, '%Y-%m-%d').month
        check_user_id = frappe.db.exists("User",{'name':user_id})
        if check_user_id:
            emp_in_user_id = frappe.db.exists("Employee",{'status':'Active','user_id':user_id})
            if emp_in_user_id:
                get_emp = frappe.db.get_value('Employee',{'name':emp_in_user_id},['designation'])
                if get_emp == "Sales Officer":
                    get_primary_monthly_target = frappe.db.sql(""" select sum(target_amount) as target_amount from `tabAmilma Target Setting` where month = '%s' and so_designation = "Sales Officer"  and type = "Secondary" """%(start_date),as_dict=1)
                elif get_emp == "Area Sales Manager":
                    get_primary_monthly_target = frappe.db.sql(""" select sum(target_amount) as target_amount from `tabAmilma Target Setting` where month = '%s' and so_designation = "Area Sales Manager"  and type = "Secondary" """%(start_date),as_dict=1)
                elif get_emp == "Regional Sales Manager":
                    get_primary_monthly_target = frappe.db.sql(""" select sum(target_amount) as target_amount from `tabAmilma Target Setting` where month = '%s' and so_designation = "Regional Sales Manager"  and type = "Secondary" """%(start_date),as_dict=1)
                else:
                    get_primary_monthly_target = ""
        return get_primary_monthly_target
    except:
        return get_primary_monthly_target           
  
def get_monthly_achieved_as_primary(user_id):
    today = nowdate()
    get_primary_monthly_achieved = ""
    posting_start_date = frappe.utils.data.get_first_day(today)
    posting_end_date = frappe.utils.data.get_last_day(today)
    start_date = datetime.strptime(today, '%Y-%m-%d').month
    try:
        get_user = frappe.db.exists("User",{'name':user_id})
        if get_user:
            get_emp = frappe.db.exists("Employee",{'status':'Active','user_id':user_id})
            if get_emp:
                get_designation = frappe.db.get_value('Employee',{'name':get_emp},['designation'])
                if get_designation == "Sales Officer":
                    get_db = frappe.db.get_value('Amilma Target Setting',{'so_designation':get_designation,'month':start_date,'type':"Primary"},['distributor'])
                    get_primary_monthly_achieved = frappe.db.sql(""" select sum(rounded_total) as monthly_achieved  from `tabSales Invoice` where customer = '%s' and posting_date between '%s' and '%s' and docstatus = 1"""
                                                    %(get_db,posting_start_date,posting_end_date))
                elif get_designation == "Area Sales Manager":
                    get_db = frappe.db.get_value('Amilma Target Setting',{'asm_designation':get_designation,'month':start_date,'type':"Primary"},['distributor'])
                    get_primary_monthly_achieved = frappe.db.sql(""" select sum(rounded_total) as monthly_achieved  from `tabSales Invoice` where customer = '%s' and posting_date between '%s' and '%s' and docstatus = 1"""
                                                    %(get_db,posting_start_date,posting_end_date))    
                elif get_designation == "Regional Sales Manager":
                    get_db = frappe.db.get_value('Amilma Target Setting',{'rsm_designation':get_designation,'month':start_date,'type':"Primary"},['distributor'])
                    get_primary_monthly_achieved = frappe.db.sql(""" select sum(rounded_total) as monthly_achieved  from `tabSales Invoice` where customer = '%s' and posting_date between '%s' and '%s' and docstatus = 1"""
                                                    %(get_db,posting_start_date,posting_end_date))   
                else:
                    get_primary_monthly_achieved = ""     
        return {"status":True,"monthly_achieved":get_primary_monthly_achieved}
    except:
        return {"status":False}

def get_monthly_achieved_as_secondary(user_id):
    today = nowdate()
    get_secondary_monthly_achieved = ""
    posting_start_date = frappe.utils.data.get_first_day(today)
    posting_end_date = frappe.utils.data.get_last_day(today)
    start_date = datetime.strptime(today, '%Y-%m-%d').month
    try:
        get_user = frappe.db.exists("User",{'name':user_id})
        if get_user:
            get_emp = frappe.db.exists("Employee",{'status':'Active','user_id':user_id})
            if get_emp:
                get_designation = frappe.db.get_value('Employee',{'name':get_emp},['designation'])
                if get_designation == "Sales Officer":
                    get_db = frappe.db.get_value('Amilma Target Setting',{'so_designation':get_designation,'month':start_date,'type':"Secondary"},['distributor'])
                    get_secondary_monthly_achieved = frappe.db.sql(""" select sum(rounded_total) as monthly_achieved  from `tabSales Invoice` where customer = '%s' and posting_date between '%s' and '%s' and docstatus = 1"""
                                                    %(get_db,posting_start_date,posting_end_date))
                elif get_designation == "Area Sales Manager":
                    get_db = frappe.db.get_value('Amilma Target Setting',{'asm_designation':get_designation,'month':start_date,'type':"Secondary"},['distributor'])
                    get_secondary_monthly_achieved = frappe.db.sql(""" select sum(rounded_total) as monthly_achieved  from `tabSales Invoice` where customer = '%s' and posting_date between '%s' and '%s' and docstatus = 1"""
                                                    %(get_db,posting_start_date,posting_end_date))    
                elif get_designation == "Regional Sales Manager":
                    get_db = frappe.db.get_value('Amilma Target Setting',{'rsm_designation':get_designation,'month':start_date,'type':"Secondary"},['distributor'])
                    get_secondary_monthly_achieved = frappe.db.sql(""" select sum(rounded_total) as monthly_achieved  from `tabSales Invoice` where customer = '%s' and posting_date between '%s' and '%s' and docstatus = 1"""
                                                    %(get_db,posting_start_date,posting_end_date))   
                else:
                    get_secondary_monthly_achieved = ""     
        return get_secondary_monthly_achieved
    except:
        return get_secondary_monthly_achieved


# def get_today_achieved_as_primary(user_id):
#     today = nowdate()
#     get_secondary_monthly_achieved = ""
#     posting_start_date = frappe.utils.data.get_first_day(today)
#     posting_end_date = frappe.utils.data.get_last_day(today)
#     start_date = datetime.strptime(today, '%Y-%m-%d').month
#     try:
#         get_user = frappe.db.exists("User",{'name':user_id})
#         if get_user:
#             get_emp = frappe.db.exists("Employee",{'status':'Active','user_id':user_id})
#             if get_emp:
#                 get_designation = frappe.db.get_value('Employee',{'name':get_emp},['designation'])
#                 if get_designation == "Sales Officer":
#                     get_db = frappe.db.get_value('Amilma Target Setting',{'so_designation':get_designation,'month':start_date,'type':"Secondary"},['distributor'])
#                     get_secondary_monthly_achieved = frappe.db.sql(""" select sum(rounded_total) as monthly_achieved  from `tabSales Invoice` where customer = '%s' and posting_date between '%s' and '%s' and docstatus = 1"""
#                                                     %(get_db,posting_start_date,posting_end_date))
#                 elif get_designation == "Area Sales Manager":
#                     get_db = frappe.db.get_value('Amilma Target Setting',{'asm_designation':get_designation,'month':start_date,'type':"Secondary"},['distributor'])
#                     get_secondary_monthly_achieved = frappe.db.sql(""" select sum(rounded_total) as monthly_achieved  from `tabSales Invoice` where customer = '%s' and posting_date between '%s' and '%s' and docstatus = 1"""
#                                                     %(get_db,posting_start_date,posting_end_date))    
#                 elif get_designation == "Regional Sales Manager":
#                     get_db = frappe.db.get_value('Amilma Target Setting',{'rsm_designation':get_designation,'month':start_date,'type':"Secondary"},['distributor'])
#                     get_secondary_monthly_achieved = frappe.db.sql(""" select sum(rounded_total) as monthly_achieved  from `tabSales Invoice` where customer = '%s' and posting_date between '%s' and '%s' and docstatus = 1"""
#                                                     %(get_db,posting_start_date,posting_end_date))   
#                 else:
#                     get_secondary_monthly_achieved = ""     
#         return get_secondary_monthly_achieved
#     except:
#         return get_secondary_monthly_achieved


def new_calls_overall_data(user_id):
    try:
        current_date = today()
        start_date = frappe.utils.data.get_first_day(today)
        end_date = frappe.utils.data.get_last_day(today)
        new_call = frappe.db.sql(""" select count(name) as total_leads from `tabLead` where creation >= """)
    except:
        pass
