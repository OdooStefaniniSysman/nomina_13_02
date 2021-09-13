# -*- coding: utf-8 -*-
# from odoo import http


# class MaintenanceThomas(http.Controller):
#     @http.route('/maintenance_thomas/maintenance_thomas/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/maintenance_thomas/maintenance_thomas/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('maintenance_thomas.listing', {
#             'root': '/maintenance_thomas/maintenance_thomas',
#             'objects': http.request.env['maintenance_thomas.maintenance_thomas'].search([]),
#         })

#     @http.route('/maintenance_thomas/maintenance_thomas/objects/<model("maintenance_thomas.maintenance_thomas"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('maintenance_thomas.object', {
#             'object': obj
#         })
