# -*- coding: utf-8 -*-
{
    'name': "Quality Todoo",

    'summary': "Calidad",

    'description': "Este modulo instala funciones y campos adicionales en el modulo de Calidad",

    'author': "Luis Felipe Paternina - Todoo SAS",
    'website': "http://www.todoo.co",
    'category': 'Tools',
    'version': '13.1.1',

        'depends': ['base','quality_control', 'hr_contract', 'sale_management'],
    
    'data': [       
         'views/quality_alert.xml',
         'views/quality_presser.xml',
         'views/quality_type_find.xml',
         'views/quality_process.xml',
         'views/quality_check.xml',
         'views/stock_move.xml',
         'security/ir.model.access.csv', 
          
    ],
    
    'demo': [
        'demo/demo.xml',
    ],
}
