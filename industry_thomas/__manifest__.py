# -*- coding: utf-8 -*-
{
    'name': "Industry Thomas",

    'summary': "Industry Thomas TST",

    'description': "Industry Thomas",

    'author': "Todoo SAS",
    'contributors': ['Luis Felipe Paternina lp@todoo.co','Carlos Guio fg@todoo.co'],
    'website': "http://www.todoo.co",
    'category': 'Tools',
    'version': '13.1',

        'depends': ['industry_fsm_report','maintenance','base_address_city','industry_fsm','contacs_thomas'],
    
    'data': [     
         'security/ir.model.access.csv',
         'security/security.xml',   
         'views/field_service.xml',
         'views/maintenance.xml',
         'views/maintenance_view.xml',
         'views/res_partner.xml',
         'views/maintenance_equipment.xml', 
         'views/sale_order.xml',
         'views/sale_order_line.xml',
         'views/res_company.xml',
         'views/res_user.xml',    
         'reports/worksheet_new.xml',
         'data/sequence.xml',
         'data/maintenance_data.xml',
         
         
        
    ],
    
    'demo': [
        'demo/demo.xml',
    ],
}
