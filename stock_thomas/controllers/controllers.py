# -*- coding: utf-8 -*-
# from odoo import http


# class StockThomas(http.Controller):
#     @http.route('/stock_thomas/stock_thomas/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/stock_thomas/stock_thomas/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('stock_thomas.listing', {
#             'root': '/stock_thomas/stock_thomas',
#             'objects': http.request.env['stock_thomas.stock_thomas'].search([]),
#         })

#     @http.route('/stock_thomas/stock_thomas/objects/<model("stock_thomas.stock_thomas"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('stock_thomas.object', {
#             'object': obj
#         })
