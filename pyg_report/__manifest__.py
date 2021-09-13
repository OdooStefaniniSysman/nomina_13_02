# -*- coding: utf-8 -*-
{
    'name': "Zpp Report",

    'summary': "Report ZPP",

    'description': "Report ZPP",

    'author': "Todoo SAS",
    'contributors': "Livingston Arias Narváez la@todoo.co",
    'website': "http://www.todoo.co",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Accounting',
    'version': '13.1',

    # any module necessary for this one to work correctly
    'depends': ['account','mrp_extended','sale_management','modify_material_purchase_requisition'],
  
    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/report_view.xml',
        'views/menuitem.xml',
    ],
}
