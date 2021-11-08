# -*- coding: utf-8 -*-
# from odoo import http


# class CrmSuprapak(http.Controller):
#     @http.route('/crm_suprapak/crm_suprapak/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/crm_suprapak/crm_suprapak/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('crm_suprapak.listing', {
#             'root': '/crm_suprapak/crm_suprapak',
#             'objects': http.request.env['crm_suprapak.crm_suprapak'].search([]),
#         })

#     @http.route('/crm_suprapak/crm_suprapak/objects/<model("crm_suprapak.crm_suprapak"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('crm_suprapak.object', {
#             'object': obj
#         })
