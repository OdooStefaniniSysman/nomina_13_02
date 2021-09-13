# -*- coding: utf-8 -*-

{
    'name' : 'Advances on Purchase Order V13 Enterprise',
    'version' : '13.0.1.0.1',
    'sequence': 201,
    'category': 'Purchase',
    'author': "Todoo SAS",
    'contributors': ['Bernardo Lara bl@todoo.co'],
    'website': "http://www.todoo.co",
    'license': '',
    'summary' : 'Module with adjustments to include Advances in the Purchases Order',
    'description' : """
        Module with adjustments to include Advances in the Purchases Order
        ==================================
    """,
    'depends': [
        'purchase',
        'account_batch_payment',
        'account_extended'
    ],
    'data' : [
         #'security/ir.model.access.csv',
         #'data/res_config_data.xml',
        #  'security/security_group.xml',
        #  'views/res_config_settings.xml',
         'views/account_payment.xml',
         'views/account_batch_payment_views.xml',
         'views/purchase_order_views.xml'
    ],
    'images': [
        "static/description/logo.png"
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
