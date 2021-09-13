# -*- coding: utf-8 -*-

{
    'name': 'Formato Impresos de Asientos Contables',
    'version': '0.1',
    'category': 'Accounting',
    'summary': 'Formato Impresos de Asientos Contables',
    'license':'AGPL-3',
    'description': """
    Formato Impresos de Asientos Contables
    """,
    'author' : 'Todoo SAS',
    'website' : 'http://www.toxtylab.com',
    'depends': [
        'account',
    ],
    'images': ['static/description/banner.jpg'],
    'data': [
        "report/reports.xml",
        "report/account_move_print_template.xml",
    ],
    'installable': True,
    'auto_install': False,
    'application': True
}

# vim:expandtab:smartindent:tabstop=2:softtabstop=2:shiftwidth=2:
