import frappe


@frappe.whitelist()
def get_masters_data():
	try:
		#get all the master data methods
		get_route_data = get_route()
		get_customer_data = get_customer()
		get_company_data = get_company()
		get_mode_of_payment_data = get_mode_of_payment()
		get_outlet_category_data = get_outlet_category()
		get_outlet_type_data = get_outlet_type()
		get_existing_type_data = get_existing_brand_volume()
		get_distributor_data = get_distributor()
		get_freezer = get_freezer_data()
		get_freezer_data_group = get_freezer_data_documents()

		masters_data_list = {
			"route_list":get_route_data,
			"outlet_list":get_customer_data,
			"company_list":get_company_data,
			"mode_of_payment_list":get_mode_of_payment_data,
			"outlet_category_list":get_outlet_category_data,
			"outlet_type_list":get_outlet_type_data,
			"existing_type_list":get_existing_type_data,
			"db":get_distributor_data,
			"freezer_data":get_freezer,
			"customer_group":get_freezer_data_group
		}
		return {"status":True,"Masters Data":masters_data_list}
	except:
		return{"status":False}

#territory master data  
def get_route():
	get_route = frappe.db.get_all('Territory',['name'])
	return get_route

#customer master data  
def get_customer():
	get_customer = frappe.db.get_all('Customer',['name'])
	return get_customer

#company master data  
def get_company():
	get_company = frappe.db.get_all('Company',['name'])
	return get_company

#Mode of payment master data
def get_mode_of_payment():
	get_payment_mode = frappe.db.get_all('Mode of Payment',{'enabled':1},['name','type'])
	return get_payment_mode

#Outlet Category master data
def get_outlet_category():
	outlet_category = frappe.db.get_all('Outlet Category',['name'])
	return outlet_category

#Outlet Type master data       
def get_outlet_type():
	outlet_type_get = frappe.db.get_all('Outlet Type',['name'])
	return outlet_type_get

#Existing Brand and Volume master data
def get_existing_brand_volume():
	get_existing_type = frappe.db.get_all('Existing Brand and Volume',['name'])
	return get_existing_type

#Customer Group master data
def get_distributor():
	get_db = frappe.db.get_all('Customer Group',['name'])
	return get_db

#freezer data master data
def get_freezer_data():
	freezer_data = frappe.db.get_all('Freezer Data',['make','model','capacity','basket','serial_no','freezer_deposit_status','freezer_deposit','transaction_reference_number','freezer_placed_date','distributor'])
	return freezer_data

@frappe.whitelist()
def get_freezer_data_documents(db):
	try:
		documents = frappe.db.get_all('Freezer Data',{'customer_group': db},['name'] )
		
		return {"status": True, "db": documents}
	except:
		
		return {"status": False}


