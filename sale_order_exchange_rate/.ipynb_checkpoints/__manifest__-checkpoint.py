# -*- coding: utf-8 -*-

{
    'name' : 'Exchange Rate per Document on Sales Order',
    'version' : '13.0.1.0.1',
    'sequence': 201,
    'category': 'Sales/Sales',
    'author': "Todoo SAS",
    'contributors': ['Jhair Escobar je@todoo.co'],
    'website': "http://www.todoo.co",
    'license': '',
    'summary' : 'Exchange Rate per Document on Sales Order',
    'description' : """
        Exchange Rate per Document on Sales Order
        ==================================
    """,
    'depends': [
        'base_setup',
        'sale_management',
        'sale_stock',
        'account_extended'
    ],
    'data' : [
         #'security/ir.model.access.csv',
         'views/sales.xml',
    ],
    'images': [
        "static/description/logo.png"
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
