# -*- coding: utf-8 -*-
{
    'name': "Account Followup Extended",

    'summary': "Account Followup Extended",

    'description': "Account Followup Extended",

    'author': "Todoo SAS",
    'contributors': ['Cristian Carreño c2@todoo.co'],
    'website': "http://www.todoo.co",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Tools',
    'version': '13.1.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'account_followup', 'account', 'account_reports', 'contacs_thomas'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/res_partner_view.xml',
        'views/account_followup_views.xml',
        'views/account_move_view.xml',
        'report/followup_sent_report_view.xml',
    ],
}
