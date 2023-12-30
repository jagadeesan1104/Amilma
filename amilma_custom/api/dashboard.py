import frappe
from frappe.utils import now,getdate,today,nowdate


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
def target_data(user_id):
    today = nowdate()
    get_primary_monthly_target = ""
    month_start_date = frappe.utils.data.get_first_day(today)
    month_end_date = frappe.utils.data.get_last_day(today)
    get_freezer_target_data = frappe.db.get_all('Amilma Target Setting', fields=['sales_officer'])
    # get_freezer_target_data = frappe.db.get_all("Amilma Target Setting",{'target_from':month_start_date,'target_to':month_end_date,"type":"Primary"},['*'])
    for target_data in get_freezer_target_data:
        if target_data.sales_officer == user_id:
            get_primary_monthly_target = frappe.db.sql(""" select sum(target_amount) as target_amount from `tabAmilma Target Setting` where target_from = '%s' and target_to = '%s' and sales_officer = '%s' and type = "Primary" """%(month_start_date,month_end_date,user_id),as_dict=1)
        elif target_data.area_sales_manager == user_id:
            get_primary_monthly_target = frappe.db.sql(""" select sum(target_amount) as target_amount from `tabAmilma Target Setting` where target_from = '%s' and target_to = '%s' and area_sales_manager = '%s' and type = "Primary" """%(month_start_date,month_end_date,user_id),as_dict=1)
        elif target_data.regional_sales_manager == user_id:
            get_primary_monthly_target = frappe.db.sql(""" select sum(target_amount) as target_amount from `tabAmilma Target Setting` where target_from = '%s' and target_to = '%s' and regional_sales_manager = '%s' and type = "Primary" """%(month_start_date,month_end_date,user_id),as_dict=1)
    return {"status":True,"primary_target":get_freezer_target_data}    

    