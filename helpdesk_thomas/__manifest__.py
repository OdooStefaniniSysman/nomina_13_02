# -*- coding: utf-8 -*-
{
    'name': "Helpdesk Thomas",

    'summary': "Help Desk Thomas",

    'description': "Help Desk Thomas",

    'author': "Todoo SAS",
    'contributors': ['Carlos Guio fg@todoo.co'],
    'website': "http://www.todoo.co",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Tools',
    'version': '13.1',

    # any module necessary for this one to work correctly
    'depends': ['base','helpdesk','contacs_thomas'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/helpdesk_team.xml',
        'views/helpdesk_thomas_view.xml',
        # 'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
