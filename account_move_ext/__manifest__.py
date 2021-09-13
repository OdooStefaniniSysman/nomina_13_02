# -*- coding: utf-8 -*-
{
    'name': "Restrincción referencia factura / Bloqueo de factura",

    'summary': "Restrincción referencia factura / Bloqueo de factura",

    'description': "Restrincción referencia factura / Bloqueo de factura",

    'author': "Todoo SAS",
    'contributors': ['Fernando Fernandez nf@todoo.co'],
    'website': "http://www.todoo.co",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Accountant',
    'version': '13.1',

    # any module necessary for this one to work correctly
    'depends': ['account_accountant'],

    # always loaded
    'data': [
        #'security/ir.model.access.csv',
        'data/account_move_groups.xml',
        'views/account_move.xml',
            
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
