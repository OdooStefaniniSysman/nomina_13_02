# -*- coding: utf-8 -*-

# Part of Probuse Consulting Service Pvt Ltd. See LICENSE file for full copyright and licensing details.

{
    'name': 'Material purchase requisitions Validations',
    'version': '1.7.2',
    'summary': """This module allow your employees/users to create Purchase Requisitions.""",
    'description': """
    
    """,
    'author': 'Todoo S.A.S',
    'contributors': ['Fernando Fernández nf@todoo.co'],
    'website': "http://www.todoo.co",
    'category': 'requisitions,purchase',
    'depends': [
                'material_purchase_requisitions_report','purchase',
                ],
    'data':[
        #'security/security.xml',
        'security/ir.model.access.csv',
        'views/purchase_requisition_view.xml',
        'views/purchase_order_view.xml',
        'views/approvals_requisition.xml',
    ],
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
