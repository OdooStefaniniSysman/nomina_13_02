# -*- coding: utf-8 -*-

{
    'name' : 'Account Bank Reconcile Restrict',
    'version' : '13.0.1.0.1',
    'sequence': 201,
    'category': 'Accounting',
    'author': "Todoo SAS",
    'contributors': ['Jhair Escobar je@todoo.co'],
    'website': "http://www.todoo.co",
    'license': '',
    'summary' : 'Account Bank Reconcile Restrict',
    'description' : """
        ==================================
    """,
    'depends': [
        'account',
    ],
    'data' : [
         'views/account_account.xml',
         'views/account_journal.xml',
    ],
    'images': [
        "static/description/logo.png"
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
