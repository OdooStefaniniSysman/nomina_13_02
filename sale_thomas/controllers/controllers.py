# -*- coding: utf-8 -*-
# from odoo import http


# class SaleThomas(http.Controller):
#     @http.route('/sale_thomas/sale_thomas/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sale_thomas/sale_thomas/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('sale_thomas.listing', {
#             'root': '/sale_thomas/sale_thomas',
#             'objects': http.request.env['sale_thomas.sale_thomas'].search([]),
#         })

#     @http.route('/sale_thomas/sale_thomas/objects/<model("sale_thomas.sale_thomas"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sale_thomas.object', {
#             'object': obj
#         })
