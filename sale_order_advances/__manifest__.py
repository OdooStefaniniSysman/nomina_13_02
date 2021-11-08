# -*- coding: utf-8 -*-

{
    'name' : 'Advances on Sales Order V13 Enterprise',
    'version' : '13.0.1.0.1',
    'sequence': 201,
    'category': 'Sales/Sales',
    'author': "Todoo SAS",
    'contributors': ['Jhair Escobar je@todoo.co'],
    'website': "http://www.todoo.co",
    'license': '',
    'summary' : 'Module with adjustments to include Advances in the Sales Order',
    'description' : """
        Module with adjustments to include Advances in the Sales Order
        ==================================
    """,
    'depends': [
        'base_setup',
        'sale_management',
        'sale_stock'
    ],
    'data' : [
         #'security/ir.model.access.csv',
         #'data/res_config_data.xml',
         'security/security_group.xml',
         'views/res_config_settings.xml',
         'views/account_payment.xml',
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
