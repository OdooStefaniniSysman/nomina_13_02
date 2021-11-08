# -*- coding: utf-8 -*-
{
    'name' : 'Account Petty Cash',
    'version': '13.0.1',
    'author': "Todoo SAS",
    'contributors': ['Jhair Escobar je@todoo.co'],
    'website': "http://www.todoo.co",
    'category': 'Accounting',
    'sequence': 20,
    'summary': 'Petty Cash management',
    'depends': ['base','sale','stock_account','account_advances','hr_expense','account'],
    'description' : """
        Ventas
        ==================================
        module for petty cash management
    """,
    'data': [
        'security/treasury_security.xml',
        'security/treasury_user_restrict_security.xml',
        'security/ir.model.access.csv',
        'wizard/treasury_box.xml',
        #'wizard/multi_reconcile_payment_views.xml',
        #'wizard/multi_reconcile_consignment_views.xml',
        #'wizard/multi_reconcile_consignment_validate_views.xml',
        'views/account_journal_view.xml',
        #'views/account_tax_view.xml',
        'views/treasury_payment_method_views.xml',
        #'views/account_payment_reconcile.xml',
        #'views/account_payment_consignment.xml',
        'views/treasury_config_view.xml',
        'views/treasury_session_view.xml',
        #'views/treasury_sequence.xml',
        'views/treasury_view.xml',
        'data/treasury_data.xml',
        'views/account_statement_view.xml',
        'views/treasury_payment.xml',
        #'views/sale_order_view.xml',
        'views/treasury_dashboard.xml',
        'views/res_users_views.xml',
        #'report/treasury_report.xml',
        #'report/treasury_session_report_template.xml'
    ],
    'demo': [
    ],
    'installable': True,
    'application': True,
}
