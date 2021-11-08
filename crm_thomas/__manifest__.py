# -*- coding: utf-8 -*-
{
    'name': "Crm Thomas",

    'summary': "Crm Thomas",

    'description': "Crm Thomas",

    'author': "Todoo SAS",
    'contributors': "Fernando Fernandez nf@todoo,co",
    'website': "http://www.todoo.co",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Sales',
    'version': '13.1',

    # any module necessary for this one to work correctly
    'depends': ['crm'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/crm_lead_view.xml',
        'views/mail_template.xml',
    ],
}
