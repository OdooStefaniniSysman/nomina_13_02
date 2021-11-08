# -*- coding: utf-8 -*-
{
    'name': "Account Advances",

    'summary': "Account Advances",

    'description': "Account Advances",

    'author': "Todoo SAS",
    'contributors': ['Jhair Escobar je@todoo.co'],
    'website': "http://www.todoo.co",
    'category': 'Accounting',
    'version': '13.1',

    'depends': ['account'],

    'data': [
        #'security/security_group.xml',
        #'security/ir.model.access.csv',
        'views/res_partner_view.xml',
        'views/account_payment_view.xml',
        'views/account_account_view.xml',
        'views/account_move_view.xml',
        'views/menu_view.xml',
        'wizards/account_move_assign_advance.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}