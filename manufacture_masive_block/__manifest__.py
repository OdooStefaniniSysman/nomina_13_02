# -*- coding: utf-8 -*-
{
    'name': "Manufacture Masive Block",

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
    'category': 'mrp',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['mrp'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/mrp_production_view.xml',
        'views/mrp_workorder_view.xml',
        #'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        #'demo/demo.xml',
    ],
}