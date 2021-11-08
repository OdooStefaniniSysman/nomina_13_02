# -*- coding: utf-8 -*-
{
    'name': "Mrp Extended",

    'summary': "- Variation Cost Mrp",

    'description': "- Variation Cost Mrp",

    'author': "Todoo SAS",
    'contributors': "Pablo Arcos pa@todoo.co, Oscar Bolaños ob@todoo.co, Fernando Fernandez nf@todoo.co, Bernardo Lara bl@todoo.co",
    'website': "http://www.todoo.co",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Manufacturing',
    'version': '13.1',

    # any module necessary for this one to work correctly
    'depends': ['mrp_account_enterprise','mrp','web_tree_dynamic_colored_field','base_vat','mrp_workorder','sale_management'],
    # always loaded
    'data': [
        'security/mrp_variation_cost_security.xml',
        'security/ir.model.access.csv',
        'data/mrp_workcenter_productivity_loss_data.xml',
        'views/mrp_workcenter_view.xml',
        'views/cost_structure_report.xml',
       # 'views/mrp_cost_structure_template.xml',
        'views/mrp_variation_view.xml',
        'views/mrp_variation_cost_menu.xml',
        #'views/mrp_variation_cost_menus.xml',
        'views/mrp_workorder_view.xml',
        'views/mrp_variation_line_view.xml',
        'views/account_line.xml',
        'views/mrp_production_view.xml',
        'views/tripulacion_view.xml',
        #'views/tripulation_form_view.xml',
        'data/accounting_groups.xml',
        'data/accounting_groups.xml',
        'views/sale_order_view.xml',
        'views/mrp_prelimit_view.xml',
        
    ],
}

