# Copyright (c) 2022, Vivek and contributors
# For license information, please see license.txt



import frappe
from frappe.utils import getdate
from datetime import datetime


def execute(filters=None):
	dd = get_period_date_ranges_columns_report(getdate(filters.get("from_date")),getdate(filters.get("to_date")))
	res = (getdate(filters.get("to_date")).year - getdate(filters.get("from_date")).year) *12 + (getdate(filters.get("to_date")).month -  getdate(filters.get("from_date")).month)

	value = ""
	if filters.get("Customer"):
		value = f""" and  si.customer = '{filters.get('Customer')}'  """
		
	dud = f""" 
                                select 
                  si.customer_name,
                                  si.freezer_serial_no,
                                  si.freezer_type,
                                  si.capacity,
                                        {dd[1]}
                  sum(si.base_grand_total) as grand,
                   DATEDIFF('{filters.get("to_date")}' , ci.creation) DIV 30 as join_moth,
                    (sum(si.base_grand_total)/( DATEDIFF('{filters.get("to_date")}' , ci.creation) DIV 30)) as avg
                from 
                  `tabSales Invoice` si
                   left join `tabCustomer` ci on ci.name =si.customer
                                        {dd[2]}

                  where si.docstatus = 1  and si.is_return = 0 and
                                                si.company = '{filters.get("company")}' and 
                                                si.posting_date between '{filters.get("from_date")}' and '{filters.get("to_date")}'
                                                {value}

                  group by si.customer_name


                                """
	# frappe.msgprint(str(dud))
	data = frappe.db.sql(f""" 
				select 
                  si.customer_name,
				  si.freezer_serial_no,
				  si.freezer_type,
				  si.capacity,
				  ci.outlet_type,
				  ci.name as cu_id,
				  ci.territory as territory,
					{dd[1]}
                  sum(si.base_grand_total) as grand,
                   DATEDIFF('{filters.get("to_date")}' , ci.creation) DIV 30 as join_moth,
	            (sum(si.base_grand_total)/( DATEDIFF('{filters.get("to_date")}' , ci.creation) DIV 30)) as avg
                from 
                  `tabSales Invoice` si
                   left join `tabCustomer` ci on ci.name =si.customer
					{dd[2]}
                  
                  where si.docstatus = 1  and si.is_return = 0 and
						si.company = '{filters.get("company")}' and 
						si.posting_date between '{filters.get("from_date")}' and '{filters.get("to_date")}'
						{value}

                  group by si.customer_name


				""",as_dict=1)
	total = 0
	count = 0
	avg=0
	for i in data:
		if i['grand']:
			total += i['grand']
		count += 1
		if i['avg']:
			avg += i['avg']
	data.append({'customer_name':"Total",'grand':total,'avg':(avg*count/100)})
	columns=[
		{
			"fieldname": "customer_name",
			"label": "<b>Customer</b>",
			"fieldtype": "Data",
			"width":  200
		},
		{
			"fieldname": "cu_id",
			"label": "<b>Customer ID</b>",
			"fieldtype": "Data",
			"width":  80
		},
		{
			"fieldname": "territory",
			"label": "<b>Territory</b>",
			"fieldtype": "Data",
			"width":  80
		},
		{
			"fieldname": "freezer_serial_no",
			"label": "<b>Serial No</b>",
			"fieldtype": "Data",
			"width":  200
		},
		{
			"fieldname": "freezer_type",
			"label": "<b>Freezer Type</b>",
			"fieldtype": "Data",
			"width":  200
		},
		{
			"fieldname": "capacity",
			"label": "<b>Freezer Size</b>",
			"fieldtype": "Data",
			"width":  200
		},
		{
			"fieldname": "outlet_type",
			"label": "<b>Outlet Type</b>",
			"fieldtype": "Data",
			"width":  200
		},
		
		

	]
	for i in dd[0]:
		columns.append(i)
	columns.append(
			{
				"fieldname": "grand",
				"label": "<b>Total </b>",
				"fieldtype": "Float",
				"default" :0.00,
				"width":  150
			}
		)
	columns.append(
                       {
                                "fieldname": "join_moth",
                                "label": "<b>Created month ago</b>",
                                "fieldtype": "Data",
                                "default" :0.00,
                                "width":  150,
								"hidden":1
                        }
                )

	columns.append(
			{
				"fieldname": "avg",
				"label": "<b>Avg</b>",
				"fieldtype": "Float",
				"default" :0.00,
				"width":  150
			}
	)

	return columns, data




@frappe.whitelist(allow_guest=True)
def get_period_date_ranges_columns_report(year_start_date,year_end_date):
	from dateutil.relativedelta import relativedelta


	res = (getdate(year_end_date).year - getdate(year_start_date).year) *12 + (getdate(year_end_date).month - getdate(year_start_date).month)
	
	increment = 1
	period_date_ranges = []
	query = ''
	row = ''
	colm = []
	
	for i in range(1, res + 2, increment):
		period_end_date = getdate(year_start_date) + relativedelta(months=increment, days=-1)
		if period_end_date > getdate(year_end_date):
			period_end_date = year_end_date

		period_date_ranges.append([year_start_date, period_end_date])

		start = getdate(year_start_date).strftime("%b%y") 
		end   = getdate(period_end_date).strftime("%b%y")

		row += f'''
				Sum({start}.base_grand_total) AS {start}g,
				''' 
		colm.append(
					{'fieldname': f'{start}g','label': f'{start}','fieldtype': 'Float','default' :0.00,'width':  150}
				)


		query += f""" \n
				LEFT JOIN `tabSales Invoice` {start} ON si.name = {start}.name 
				and si.posting_date between '{year_start_date}' 
				and '{period_end_date}' 
				   """

		year_start_date = period_end_date + relativedelta(days=1)
		if period_end_date == year_end_date:
			break
	return [colm,row,query]

