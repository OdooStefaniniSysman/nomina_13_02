# -*- coding: utf-8 -*-
{
    'name': "Única Descripción cuenta analítica / Adición de segmentos",

    'summary': "Única Descripción cuenta analítica / Adición de segmentos",

    'description': "Única Descripción cuenta analítica / Adición de segmentos",

    'author': "Todoo SAS",
    'contributors': ['Fernando Fernandez nf@todoo.co'],
    'website': "http://www.todoo.co",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Accountant',
    'version': '13.1',

    # any module necessary for this one to work correctly
    'depends': ['account_accountant'],

    # always loaded
    'data': [
        #'security/ir.model.access.csv',
        'views/account_analytic_group.xml',
        'views/account_analytic_segment.xml',
        'views/account_analytic_segment_report.xml',
        'views/account_analytic_account_view.xml',
        'security/ir.model.access.csv',
    ],
    # only loaded in demonstration mode
}