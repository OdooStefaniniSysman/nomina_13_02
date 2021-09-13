{
    'name': 'Generate Checks Thomas',
    'version': '13',
    'author': "Todoo",
    'contributors': ['Luis Felipe Paternina lp@todoo.co'],
    'website': "www.todoo.com",
    'category': 'Account',
    'depends': [
        'account_accountant',
        'account_check_printing',
    ],
    'data': [
        #'security/ir.model.access.csv',    
        'views/account_journal.xml',
        'views/account_payment.xml',        
    ],
    'installable': True
}