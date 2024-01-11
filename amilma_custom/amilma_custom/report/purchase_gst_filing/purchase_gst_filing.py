# Copyright (c) 2024, Vivek and contributors
# For license information, please see license.txt

import frappe
from frappe import _, msgprint
import re
from frappe.utils import get_first_day, today, get_last_day, format_datetime, add_years, date_diff, add_days, getdate, cint, format_date,get_url_to_form


def execute(filters=None):
	columns = get_columns(filters)
	data = get_data(filters)
	return columns, data



# giving the columns below for report
def get_columns(filters):
	columns = [
		_("Outlet Name") + ":Data:200",
		_("GST No") + ":Data:150",
		_("Bill Date") + ":Data:120",
		_("Bill No") + ":Data:200",
		_("Bill Amount") + ":Data:100",
		_("SGST") + ":Currency:100",
		_("CGST") + ":Currency:100",
		_("IGST") + ":Currency:100",
		_("Total Amount") +":Currency:150"
	]
	return columns




#getting the purchase invoice data
def get_data(filters):
	data = []
	if filters.company:
		get_purchase_invoice = frappe.db.get_all("Purchase Invoice",{'docstatus':1,'posting_date':('between',(filters.from_date,filters.to_date)),'company':filters.company},['supplier_name','tax_id','posting_date','name','base_net_total','rounded_total'])
	else:
		get_purchase_invoice = frappe.db.get_all("Purchase Invoice",{'docstatus':1,'posting_date':('between',(filters.from_date,filters.to_date))},['supplier_name','tax_id','posting_date','name','base_net_total','rounded_total'])
	for purchase in get_purchase_invoice:
			sgst_tax_amount = get_sgst_tax_amount(purchase.name)
			cgst_tax_amount = get_cgst_tax_amount(purchase.name)
			igst_tax_amount = get_igst_tax_amount(purchase.name)
			row = [purchase.supplier_name,purchase.tax_id,format_date(purchase.posting_date),purchase.name,purchase.base_net_total,sgst_tax_amount,cgst_tax_amount,igst_tax_amount,purchase.rounded_total]
			data.append(row)
	return data	

# get the purchase taxes table in thata if sgst is here get the tax_amount 
def get_sgst_tax_amount(name):
	get_tax_amount = 0
	tax_account = frappe.db.get_all("Purchase Taxes and Charges",{'parent':name},['account_head'])
	for tax in tax_account:
		pattern = re.compile(r'\bSGST\b')
		matches = pattern.findall(tax.account_head)
		if matches == ["SGST"]:
			get_tax_amount = frappe.db.get_value("Purchase Taxes and Charges",{'parent':name,'account_head':tax.account_head},['tax_amount']) or 0
			return get_tax_amount

# get the purchase taxes table in thata if cgst is here get the tax_amount 
def get_cgst_tax_amount(name):
	get_tax_amount = 0
	tax_account = frappe.db.get_all("Purchase Taxes and Charges",{'parent':name},['account_head'])
	for tax in tax_account:
		pattern = re.compile(r'\bCGST\b')
		matches = pattern.findall(tax.account_head)
		if matches == ["CGST"]:
			get_tax_amount = frappe.db.get_value("Purchase Taxes and Charges",{'parent':name,'account_head':tax.account_head},['tax_amount']) or 0
			return get_tax_amount		

# get the purchase taxes table in thata if igst is here get the tax_amount 
def get_igst_tax_amount(name):
	get_tax_amount = 0
	tax_account = frappe.db.get_all("Purchase Taxes and Charges",{'parent':name},['account_head'])
	for tax in tax_account:
		pattern = re.compile(r'\bIGST\b')
		matches = pattern.findall(tax.account_head)
		if matches == ["IGST"]:
			get_tax_amount = frappe.db.get_value("Purchase Taxes and Charges",{'parent':name,'account_head':tax.account_head},['tax_amount']) or 0
			return get_tax_amount
		