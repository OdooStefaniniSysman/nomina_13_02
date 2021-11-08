# -*- coding: utf-8 -*-
{
    'name': "Unique Supplier Invoice Number in Invoice",

    'summary': "Unique Supplier Invoice Number in Invoice",

    'description': "Unique Supplier Invoice Number in Invoice",

    'author': "Todoo SAS",
    'contributors': ['Fernando Fernandez nf@todoo.co'],
    'website': "http://www.todoo.co",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Accountant',
    'version': '13.1',

    # any module necessary for this one to work correctly
    'depends': ['account'],

    # always loaded
    'data': [
        'views/account_move_view.xml',
    ],
}
