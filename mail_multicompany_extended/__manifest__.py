# -*- coding: utf-8 -*-
{
    'name': "Email Multi company",

    'summary': "Email Multi company",

    'description': "Email Multi company",

    'author': "Todoo S.A.S.",
    'website': "http://www.todoo.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Extra Tools',
    'version': '13.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/res_partner_view.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'pre_init_hook': 'pre_init_hook',
    'post_init_hook': 'post_init_hook',
    # 'uninstall_hook': 'uninstall_hook',
}
