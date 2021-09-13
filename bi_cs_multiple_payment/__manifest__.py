# -*- coding: utf-8 -*-
# Part of Browseinfo. See LICENSE file for full copyright and licensing details.
{
	'name': 'Multiple Invoice Payment(Customer/Supplier)',
	'version': '11.0.0.1',
	'category': 'Accounting',
	'sequence': 15,
    'summary': 'This apps help to make single payment for multiple invoices together',
    'description': """
    	Multiple Invoice Payment
    	for Customer and Supplier
    	customer invoice payment, supplier invoice payment.
    	single payment from multiple invoice
    	multiple customer invoice payment
    	multiple supplier invoice payment
    	multiple payment option
    	payment invoice
    	multi invoice payment
    	multi sale order payment
    	many invoice payment, payment register for multiple invoice
    	multiple bill payment, multiple vendor bill payment, multiple vendor bill single payment
    	multiple payment receipt for multiple invoice,  multiple payment receipt for many invoice

""",
	'author' : 'Browseinfo',
	'website': 'http://www.browseinfo.in',
	'price': 25.00,
    	'currency': "EUR",
	'depends': ['account','account','account_payment'],
	'data': [
	'wizard/multi_invoice_payment_views.xml',
	'views/multi_payment_views.xml',
	],
	'demo': [],
	'css': [],
	'installable': True,
	'auto_install': False,
	'application': False,
	'live_test_url':'https://youtu.be/gyCl9Ru5rMY',
    	"images":['static/description/Banner.png'],
}
