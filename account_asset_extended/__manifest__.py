# -*- coding: utf-8 -*-
{
    'name': "Account Asset Extended",

    'summary': """
        Extended module for account asset 
    """,

    'description': """
        Extended module for account asset
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
    'depends': ['account_asset','product','hr','product_category_reference'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        # 'views/views.xml',
        'views/server_actions.xml',
        'views/account_asset.xml',
        'views/product_template.xml',
        'views/asset_movements_views.xml',
        'report/asset_report.xml',
        'report/account_assets_report_views_extended.xml',
        'wizards/dismantlement_move_wizard.xml',
        'wizards/asset_pause_views.xml',
        'wizards/asset_modify_views.xml',
        # 'wizards/asset_sell_views.xml',
        'wizards/asset_valorization_view.xml',
        'wizards/asset_modify_model_view.xml',
        'wizards/asset_modify_masive_views.xml',
    ],
}
