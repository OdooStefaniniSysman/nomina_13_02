# -*- coding: utf-8 -*-
{
    'name': "Intercompany Payments",

    'summary': """
        This module allows to make payments and boys betwen internal companies
        """,

    'description': """
        This module allows to make payments and boys betwen internal companies
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
    'depends': ['inter_company_rules'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/account_journal.xml',
        'views/purchase_order.xml',
    ],
}
