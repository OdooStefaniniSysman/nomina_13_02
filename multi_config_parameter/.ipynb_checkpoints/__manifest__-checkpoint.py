# -*- coding: utf-8 -*-

{
    'name' : 'Multi System Parameters',
    'version' : '13.0.1.0.1',
    'sequence': 201,
    'category': 'Sales/Sales',
    'author': "Todoo SAS",
    'contributors': ['Jhair Escobar je@todoo.co'],
    'website': "http://www.todoo.co",
    'license': '',
    'summary' : 'Adds multi-company and multi-website support',
    'description' : """
        Adds multi-company and multi-website support
        ==================================
    """,
    'depends': [
        'web_multi_base',
        'mail',
        'fetchmail'
    ],
    "uninstall_hook": "uninstall_hook",
    'installable': True,
    'application': True,
    'auto_install': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
