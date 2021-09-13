# -*- coding: utf-8 -*-
# from odoo import http


# class HelpDeskThomas(http.Controller):
#     @http.route('/help_desk_thomas/help_desk_thomas/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/help_desk_thomas/help_desk_thomas/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('help_desk_thomas.listing', {
#             'root': '/help_desk_thomas/help_desk_thomas',
#             'objects': http.request.env['help_desk_thomas.help_desk_thomas'].search([]),
#         })

#     @http.route('/help_desk_thomas/help_desk_thomas/objects/<model("help_desk_thomas.help_desk_thomas"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('help_desk_thomas.object', {
#             'object': obj
#         })
