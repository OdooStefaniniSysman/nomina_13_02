# -*- coding: utf-8 -*-
{
    'name': "Txt generator for payment in banking portal",

    'summary': """
        It allows to generate TXT file to upload the payment to the banking portal""",

    'description': """
        It allows to generate TXT file to upload the payment to the banking portal
    """,

    'author': "Bernardo D. Lara Guevara bl@todoo.co",
    'website': "https://www.todoo.co",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Accounting/Accounting',
    'version': '13.0.1',

    # any module necessary for this one to work correctly
    'depends': ['account_batch_payment'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/res_bank_txt_config_views.xml',
        'views/account_batch_payment_views.xml',
        'views/payment_type_views.xml',
        'wizards/payment_txt_generator_wizard_views.xml',
    ],
}
