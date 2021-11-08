# -*- coding: utf-8 -*-

{
    'name': 'Formato Impreso Registro Diferencia en Cambio',
    'version': '13.0.1',
    'category': 'Accounting',
    'summary': 'Formato Impresos de diferencia en cambio en Pagos',
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
        "report/payment_currency_exchange_print.xml",
    ],
    'installable': True,
    'auto_install': False,
    'application': False
}