from . import __version__ as app_version

app_name = "amilma_custom"
app_title = "Amilma Custom"
app_publisher = "Vivek"
app_description = "Custom Development"
app_email = "vivekchamp84@gmail.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/amilma_custom/css/amilma_custom.css"
# app_include_js = "/assets/amilma_custom/js/amilma_custom.js"

# include js, css files in header of web template
# web_include_css = "/assets/amilma_custom/css/amilma_custom.css"
# web_include_js = "/assets/amilma_custom/js/amilma_custom.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "amilma_custom/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
doctype_js = {
    "Sales Order" : "public/js/sales_order.js"
    }
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
#	"methods": "amilma_custom.utils.jinja_methods",
#	"filters": "amilma_custom.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "amilma_custom.install.before_install"
# after_install = "amilma_custom.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "amilma_custom.uninstall.before_uninstall"
# after_uninstall = "amilma_custom.uninstall.after_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "amilma_custom.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
#	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
#	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
#	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"Lead": {
# 		"on_update": "amilma_custom.api.new_call.update_shop_image_lead",
# 	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
#	"all": [
#		"amilma_custom.tasks.all"
#	],
#	"daily": [
#		"amilma_custom.tasks.daily"
#	],
#	"hourly": [
#		"amilma_custom.tasks.hourly"
#	],
#	"weekly": [
#		"amilma_custom.tasks.weekly"
#	],
#	"monthly": [
#		"amilma_custom.tasks.monthly"
#	],
# }

# Testing
# -------

# before_tests = "amilma_custom.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
#	"frappe.desk.doctype.event.event.get_events": "amilma_custom.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
#	"Task": "amilma_custom.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]


# User Data Protection
# --------------------

# user_data_fields = [
#	{
#		"doctype": "{doctype_1}",
#		"filter_by": "{filter_by}",
#		"redact_fields": ["{field_1}", "{field_2}"],
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_2}",
#		"filter_by": "{filter_by}",
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_3}",
#		"strict": False,
#	},
#	{
#		"doctype": "{doctype_4}"
#	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
#	"amilma_custom.auth.validate"
# ]


fixtures = [{
    "dt": "Custom Field",
    "filters": [
        ["name", "in", [
            #Employee Checkin Custom Field
            'Employee Checkin-custom_image','Employee Checkin-custom_punch_date','Employee Checkin-custom_work_done','Employee Checkin-custom_employee_route'

            #opportunity Custom Field
            ,'Opportunity-custom_existing_brand_and_volume','Opportunity-custom_outlet_type','Opportunity-custom_outlet_category'

            #Customer Custom Field
            'Customer-custom_outlet_type','Customer-custom_outlet_category','Customer-outlet_type_abbr','Customer-customer_status','Customer-custom_db',
            'Customer-outlet_type_abbr','Customer-custom_new_call_details','Customer-custom_outlet_name','Customer-custom_shop_daily_sales',
            'Customer-custom_existing_brand','Customer-custom_ice_cream_sales','Customer-custom_column_break_1nzvh','Customer-custom_shop_outside_image',
            'Customer-custom_shop_inside_image','Customer-custom_longitude','Customer-custom_column_break_zaquo','Customer-custom_live_location','Customer-custom_latitude',
            'Customer-custom_gps_details',

            #Lead Custom Field
            'Lead-ice_cream_sales','Lead-custom_existing_ice_cream_brand','Lead-shop_daily_sales','Lead-custom_outlet_category',
            'Lead-custom_outlet_type','Lead-tgr5','Lead-db','Lead-outlet_details','Lead-section_break_0','Lead-customer_group',
            'Lead-custom_shop_inside_image','Lead-custom_shop_outside_image','Lead-custom_outlet_address','Lead-custom_live_location','Lead-custom_longitude',
            'Lead-custom_column_break_8tavo','Lead-custom_latitude','Lead-custom_gps_details'

            #Contact Custom Field
            'Contact-custom_aaadhar_number'

            #Sales order
            'Sales Order-custom_api_method_marked'
        ]]
    ]
    },
    {
        "dt":"Property Setter",
        "filters":[
            ["name","in",[
                "Employee Checkin-main-field_order","Employee Checkin-main-image_field","Employee-main-field_order",
                'Sales Invoice-base_rounded_total-in_list_view'
            ]]
        ]

    }]
