# -*- coding: utf-8 -*-
# from odoo import http


# class IntercompanyPayments(http.Controller):
#     @http.route('/intercompany_payments/intercompany_payments/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/intercompany_payments/intercompany_payments/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('intercompany_payments.listing', {
#             'root': '/intercompany_payments/intercompany_payments',
#             'objects': http.request.env['intercompany_payments.intercompany_payments'].search([]),
#         })

#     @http.route('/intercompany_payments/intercompany_payments/objects/<model("intercompany_payments.intercompany_payments"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('intercompany_payments.object', {
#             'object': obj
#         })
