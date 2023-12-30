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

@frappe.whitelist()
def target_setting(user_id):
    today = nowdate()
    status = ""
    try:
        get_primary_monthly_target = ""
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
                    status = False
            else:
                status = False
        else:
            status = False
        return {"status":status,"primary_target":get_primary_monthly_target,}     
    except:
        status = False
        return {"status":status}           
  

    