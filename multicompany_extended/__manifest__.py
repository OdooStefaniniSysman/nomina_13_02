# -*- coding: utf-8 -*-
{
    'name': "Multicompany extended",

    'summary': "Multicompany extended",

    'description': "Multicompany extended",

    'contributors': 'Juan Arcos juanparmer@gmail.com',
    'author': "Todoo S.A.S.",
    'website': "http://www.todoo.co",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Technical Settings',
    'version': '13.1',

    # any module necessary for this one to work correctly
    'depends': [
        'crm',
        'helpdesk',
        'product',
        'project',
        'survey',
    ],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'security/crm_crm.xml',
        'security/helpdesk_helpdesk.xml',
        'security/product_product.xml',
        'security/project_project.xml',
        'security/survey_survey.xml',
        'views/crm_crm_view.xml',
        'views/helpdesk_helpdesk_view.xml',
        'views/product_product_view.xml',
        'views/project_project_view.xml',
        'views/survey_survey_view.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        #'demo/demo.xml',
    ],
}
