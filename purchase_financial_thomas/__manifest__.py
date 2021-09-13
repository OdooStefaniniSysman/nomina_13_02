{
    'name': 'Purchase Financial Thomas',
    'version': '13',
    'author': "Todoo SAS",
    'website': "www.todoo.com",
    'category': 'Purchase',
    'depends': [
        'purchase',
    ],
    'data': [
        #'security/ir.model.access.csv', 
        #Luis Felipe Paternina Vital     
        'views/purchase.xml',
        'reports/purchase_order.xml',         
    ],
    'installable': True
}