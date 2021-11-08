{
    'name': 'account analytic financial thomas',
    'version': '13',
    'author': "Todoo",
    'contributors': ['Luis Felipe Paternina lp@todoo.co'],
    'website': "www.todoo.co",
    'category': 'account',
    'depends': [
        'account_accountant',
        'analytic',
        'l10n_co',
        'l10n_co_reports',
        'account_asset_extended',
    ],
    'data': [
        #'security/ir.model.access.csv',     
        'views/account_analytic.xml',
        'views/account_account_replace.xml',
        'views/account_account.xml',
        'views/account_move.xml',
        #'views/product.xml',         
    ],
    'installable': True
}