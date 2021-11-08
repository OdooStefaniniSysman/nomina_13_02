# -*- coding: utf-8 -*-
{
    'name': "Mail Notification Currency Change",

    'summary': """
        This module send a mail when the rate in currency rate is changed
        """,

    'description': """
        This module send a mail when the rate in currency rate is changed
    """,

    'author': "Todoo SAS",
    'contributors': ['Carlos Guio fg@todoo.co'],
    'website': "http://www.todoo.co",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Tools',
    'version': '13.1',

    # any module necessary for this one to work correctly
    'depends': ['currency_rate_live'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'data/res_groups.xml',
        'data/mail_data.xml',
        # 'views/account_move.xml',
    ],
}
