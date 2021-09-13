# -*- coding: utf-8 -*-
{
    'name': "Helpdesk Thomas",

    'summary': "Help Desk Thomas",

    'description': "Help Desk Thomas",

    'author': "Todoo SAS",
    'contributors': ['Fernando Fernández nf@todoo.co'],
    'website': "http://www.todoo.co",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Tools',
    'version': '13.1',

    # any module necessary for this one to work correctly
    'depends': ['base','helpdesk','helpdesk_sale','crnd_web_float_full_time_widget','website'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/management_helpdesk.xml',
        'data/helpdesk_team.xml',
        'views/helpdesk_thomas_view.xml',
        'views/helpdesk_thomas_service_view.xml',
        'views/helpdesk_thomas_subservice_view.xml',
        'views/helpdesk_thomas_group_users.xml',
        'views/helpdesk_thomas_type_ticket.xml',
        'views/helpdesk_thomas_activity.xml',
        'views/helpdesk_thomas_material_type.xml',
        'views/helpdesk_thomas_material.xml',
        'views/helpdesk_thomas_escoltas.xml',
        'views/helpdesk_thomas_departament.xml',
        'views/helpdesk_thomas_team_helpdesk.xml',
        'views/helpdesk_thomas_personas.xml',
        'views/helpdesk_thomas_producto.xml',
        'views/helpdesk_thomas_producto_muestras.xml',
        'views/helpdesk_thomas_ans.xml',
        'views/helpdesk_thomas_portal_template.xml',
        'template/helpdesk_solved.xml',
        #'views/helpdesk_thomas_mesas_ayuda_kanban.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
