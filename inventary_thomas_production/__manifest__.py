# -*- coding: utf-8 -*-
{
    'name': "Inventory Thomas Production",

    'summary': """
        this is the module to configure Stock Module""",

    'description': """

    """,

    'author': "Todoo SAS",
    'contributors': ['Livingston Arias Narváez la@todoo.co'],
    'website': "http://www.todoo.co",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Stock',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['stock_account'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/stock_inventory_view.xml',
        'views/stock_quant_view.xml',
        #'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        #'demo/demo.xml',
    ],
}
