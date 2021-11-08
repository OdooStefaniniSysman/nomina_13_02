# -*- coding: utf-8 -*-
{
    'name': "two_purchase_approval",

    'summary': """
        This module generate two approval for purchase module""",

    'description': """

    """,

    'author': "Todoo SAS",
    'contributors': ['Livingston Arias Narváez la@todoo.co'],
    'website': "http://www.todoo.co",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Purchase',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['purchase'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/purchase_order_view.xml',
        'wizard/two_purchase_approval_wizard_view.xml',
        #'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        #'demo/demo.xml',
    ],
}