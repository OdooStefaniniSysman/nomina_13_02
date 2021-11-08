# -*- coding: utf-8 -*-
# from odoo import http


# class CrmThomas(http.Controller):
#     @http.route('/crm_thomas/crm_thomas/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/crm_thomas/crm_thomas/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('crm_thomas.listing', {
#             'root': '/crm_thomas/crm_thomas',
#             'objects': http.request.env['crm_thomas.crm_thomas'].search([]),
#         })

#     @http.route('/crm_thomas/crm_thomas/objects/<model("crm_thomas.crm_thomas"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('crm_thomas.object', {
#             'object': obj
#         })
