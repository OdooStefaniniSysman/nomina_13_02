{
    'name': 'Account Payment Purse Thomas',
    'version': '13',
    'author': "Todoo SAS",
    'website': "www.todoo.co",
    'category': 'Purse',
    'depends': [
        'account_accountant',
        'partner_bank_in_payment',
    ],
    'data': [
        #'security/ir.model.access.csv',   
        'views/account_payment.xml',        
    ],
    'installable': True
}