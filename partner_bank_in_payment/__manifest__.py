# -*- coding: utf-8 -*-
{
    'name': "Partner Bank in Payments",

    'summary': """
        This module allows a bank account to be seen in payments
        """,

    'description': """
        This module allows a bank account to be seen in payments
    """,

    'author': "Todoo SAS",
    'contributors': ['Carlos Guio fg@todoo.co'],
    'website': "http://www.todoo.co",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Tools',
    'version': '13.1.1',

    # any module necessary for this one to work correctly
    'depends': ['account','account_batch_payment'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/account_payment.xml',
        'views/account_move.xml',
        'views/account_batch_payment.xml',
        'views/partner_view.xml',
        # 'views/templates.xml',
    ],
}
