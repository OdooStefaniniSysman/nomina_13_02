# -*- coding: utf-8 -*-

{
    'name' : 'Exchange Rate per Document on Purchase Order',
    'version' : '13.0.1.0.1',
    'sequence': 201,
    'category': 'Purchase',
    'author': "Todoo SAS",
    'contributors': ['Bernardo Lara bl@todoo.co'],
    'website': "http://www.todoo.co",
    'license': '',
    'summary' : 'Exchange Rate per Document on Purchase Order',
    'description' : """
        Exchange Rate per Document on Purchase Order
        ==================================
    """,
    'depends': [
        'base_setup',
        'purchase',
        'account_extended'
    ],
    'data' : [
         #'security/ir.model.access.csv',
         'views/account_move.xml',
         'views/purchase_order_views.xml',
    ],
    'images': [
        "static/description/logo.png"
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
