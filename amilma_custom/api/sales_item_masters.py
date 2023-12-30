import frappe
from erpnext.stock.utils import get_stock_balance


@frappe.whitelist()
def get_sales_master_items(company):
    try:
        item_groups = ['Ice Creams', 'Endless', 'Pop Material', 'Accessories']
        items_in_group = frappe.db.get_all('Item', filters={'item_group': ['in', item_groups]}, fields=['name', 'item_name'])
        formatted_item_list = []

        for item in items_in_group:
            item_price_list = get_item_price_list(item.name)
            get_warehouse = get_item_warehouse(company)
            stock_balance = get_stock_balance(item.name, get_warehouse)
            if stock_balance > 0.0:
                masters_data = {
                    "name": item.name,
                    "item_name": item.item_name,
                    "item_price": item_price_list,
                    "avail_qty": stock_balance
                }
                formatted_item_list.append(masters_data)
        return {"status": True, "sales_item_masters": formatted_item_list}
    except Exception as e:
        return {"status": False, "message": str(e)}

# below getting the get item price
def get_item_price_list(item_code):
    item_price_list = frappe.db.get_value('Item Price', {'item_code': item_code, 'selling': 1}, 'price_list_rate')
    return item_price_list

def get_item_warehouse(company):
    warehouse = frappe.db.get_value('Warehouse', {'company': company, 'warehouse_name': 'Stores'}, ['name'])
    return warehouse
