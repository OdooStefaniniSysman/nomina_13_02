# -*- coding: utf-8 -*-
{
    'name': "Sale Thomas",

    'summary': "Sale Thomas",

    'description': "Sale Thomas",

    'author': "Todoo SAS",
    'contributors': ['Carlos Guio fg@todoo.co'],
    'website': "http://www.todoo.co",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Tools',
    'version': '13.1',

    # any module necessary for this one to work correctly
    'depends': ['sale','sale_management', 'contacs_thomas', 'industry_thomas'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/sales_thomas.xml',
        'views/account_move_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
