# -*- coding: utf-8 -*-
{
    'name': "Alternate Payment Receiver",

    'summary': """
        Alternative person in payment
        """,

    'description': """
        Alternative person in payment
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
    'depends': ['account','contacts'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/res_partner.xml',
        'views/res_partner_alternative_person.xml',
        'views/account_payment.xml',
        'reports/payment_report.xml',
    ],
}
