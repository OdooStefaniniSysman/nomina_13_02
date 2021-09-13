# -*- coding: utf-8 -*-
{
    'name': "Account extended",

    'summary': "Account extended",

    'description': "Account extended",

    'author': "Todoo SAS",
    'contributors': [
        'Pablo Arcos pa@todoo.co', 
        'Carlos Guio cg@todoo.co'
        'Jhair Escobar je@todoo.co'
        'Cristian Carreño je@todoo.co'
    ],
    'website': "http://www.todoo.co",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Accounting/Accounting',
    'version': '13.1.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'account','account_reports','mail'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/account_security.xml',
        'views/account_view.xml',
        'views/account_fiscal_position_view.xml',
        'views/account_journal_view.xml',
        'views/account_move_view.xml',
        'views/res_config_settings_views.xml',
        'views/account_invoice_view.xml',
        'views/account_payment_approvals_view.xml',
        'views/account_payment_view.xml',
        'views/account_type_view.xml',
        'views/templates.xml',
        'views/account_bank_statement_view.xml',
        'views/account_payment_report.xml',
        'views/product_concept_type.xml',
        'views/product_view.xml',
        'data/data.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
