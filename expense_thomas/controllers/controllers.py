# -*- coding: utf-8 -*-
# from odoo import http


# class ExpenseThomas(http.Controller):
#     @http.route('/expense_thomas/expense_thomas/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/expense_thomas/expense_thomas/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('expense_thomas.listing', {
#             'root': '/expense_thomas/expense_thomas',
#             'objects': http.request.env['expense_thomas.expense_thomas'].search([]),
#         })

#     @http.route('/expense_thomas/expense_thomas/objects/<model("expense_thomas.expense_thomas"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('expense_thomas.object', {
#             'object': obj
#         })
