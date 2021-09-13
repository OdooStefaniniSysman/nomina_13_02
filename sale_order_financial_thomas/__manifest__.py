{
    'name': 'Sale Order Financial Thomas',
    'version': '13',
    'author': "Todoo SAS",
    'website': "www.todoo.co",
    'contributors': ['Luis Felipe Paternina lp@todoo.co'],
    'category': 'Sales',
    'depends': [
        'sale_management',
        'account_accountant',
        'l10n_co_e_invoicing_comfiar',
    ],
    'data': [
        #'security/ir.model.access.csv', 
        #Luis Felipe Paternina Vital     
        'views/sale_order.xml',
        'views/account_move.xml',
        'views/res_partner_views.xml',
    ],
    'installable': True
}