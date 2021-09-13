# -*- coding: utf-8 -*-

{
    'name': 'Control de Radicación en Facturas',
    'version': '13.0.1',
    'category': 'Accounting',
    'summary': 'Control de Radicación de Facturas',
    'license':'AGPL-3',
    'description': """
    """,
    'author' : 'Todoo SAS',
    'website' : 'http://www.todoo.co',
    'depends': [
        'account_extended',
    ],
    'images': ['static/description/banner.jpg'],
    'data': [
        "security/security_group.xml",
        #"security/ir.model.access.csv",
        "views/account_invoice_view.xml",
        "views/multi_filed_view.xml",
        "wizard/action_multi_filed_view.xml",
    ],
    'installable': True,
    'auto_install': False,
    'application': False
}

# vim:expandtab:smartindent:tabstop=2:softtabstop=2:shiftwidth=2:
