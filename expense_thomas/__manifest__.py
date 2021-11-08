# -*- coding: utf-8 -*-
{
    'name': "Expense Thomas",

    'summary': "Expense Thomas",

    'description': "Expense Thomas",

    'author': "Todoo SAS",
    'contributors': ['Carlos Guio fg@todoo.co'],
    'website': "http://www.todoo.co",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Tools',
    'version': '13.1',

    # any module necessary for this one to work correctly
    'depends': ['base',
                'hr_expense',
                'contacs_thomas',
                'maintenance_thomas',
                'sign'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/expense_thomas_view.xml',
        'views/advances_assigment_thomas.xml',
        'views/server_actions.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
