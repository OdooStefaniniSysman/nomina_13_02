# -*- coding: utf-8 -*-
{
    'name': "Block CRUD",

    'summary': "Block CRUD",

    'description': "Block CRUD",

    'author': "Todoo SAS",
    'contributors': ['Jhair Escobar je@todoo.co'],
    'website': "http://www.todoo.co",

    'category': 'Tools',
    'version': '13.1',

    # any module necessary for this one to work correctly
    'depends': ['account', 'mrp', 'sale', 'purchase', 'material_purchase_requisitions','hr_payroll'],

    # always loaded
    'data': [
        #'security/ir.model.access.csv',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
