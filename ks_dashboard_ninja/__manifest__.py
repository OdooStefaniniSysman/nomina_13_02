# -*- coding: utf-8 -*-
{
    'name': "Dashboard Ninja",

    'summary': """
    Revamp your Odoo Dashboard like never before! It is one of the best dashboard odoo apps in the market.
    """,

    'description': """
        Dashboard Ninja v11.0,
        Odoo Dashboard, 
        Dashboard,
        Odoo apps,
        Dashboard app,
        HR Dashboard,
        Sales Dashboard, 
        inventory Dashboard, 
        Lead Dashboard, 
        Opportunity Dashboard, 
        CRM Dashboard,
    """,

    'author': "Ksolves",
    'license': 'OPL-1',
    'currency': 'EUR',
    'price': 99.0,
    'website': "https://www.ksolves.com",
    'maintainer': 'Ksolves India Pvt. Ltd.',
    'live_test_url': 'https://www.youtube.com/watch?v=vWjKCwlyMdE',
    'category': 'Tools',
    'version': '3.1.0',
    'support': 'sales@ksolves.com',
    'images': ['static/description/main.png'],

    'depends': ['base', 'web', 'base_setup','sale_management'],

    'data': [
        'security/ks_security_groups.xml',
        'security/ir.model.access.csv',
        'data/ks_sales_data.xml',
        'data/ks_default_data.xml',
        'views/ks_dashboard_ninja_view.xml',
        'views/ks_dashboard_ninja_item_view.xml',
        'views/ks_dashboard_ninja_assets.xml',
        'views/ks_dashboard_action.xml',
    ],

    'qweb': [
        'static/src/xml/ks_dashboard_ninja_templates.xml',
        'static/src/xml/ks_dashboard_ninja_item_templates.xml',
        'static/src/xml/ks_dashboard_ninja_item_theme.xml',
        'static/src/xml/ks_widget_toggle.xml',
        'static/src/xml/ks_dashboard_pro.xml',
    ],

    'uninstall_hook': 'uninstall_hook',

}
