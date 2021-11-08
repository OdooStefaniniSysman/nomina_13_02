# -*- coding: utf-8 -*-

{
    'name': 'Formato Impreso Comprobante de Egreso',
    'version': '13.0.1',
    'category': 'Accounting',
    'summary': 'Formato Impresos de Comprobante de Egreso',
    'license':'AGPL-3',
    'description': """
    """,
    'author' : 'Todoo SAS',
    'contributors': ['Luis Felipe Paternina lp@todoo.co'],
    'website' : 'http://www.todoo.co',
    'depends': [
        'account_accountant',
    ],
    'images': ['static/description/banner.jpg'],
    'data': [
        "report/reports.xml",
        "report/account_payment_print.xml",
    ],
    'installable': True,
    'auto_install': False,
    'application': False
}