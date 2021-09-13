{
    'name': 'Report Book Day Financial',
    'version': '13',
    'author': "Todoo SAS",
    'contributors': ['Luis Felipe Paternina lp@todoo.co'],
    'website': "www.todoo.co",
    'category': 'reports',
    'depends': [
        'account_accountant',
    ],
    'data': [
        #'security/ir.model.access.csv', 
        #Luis Felipe Paternina Vital     
        'views/account_move_line.xml',        
    ],
    'installable': True
}