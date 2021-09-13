# -*- coding: utf-8 -*-
# from odoo import http


# class ReconcilieModelPartner(http.Controller):
#     @http.route('/reconcilie_model_partner/reconcilie_model_partner/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/reconcilie_model_partner/reconcilie_model_partner/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('reconcilie_model_partner.listing', {
#             'root': '/reconcilie_model_partner/reconcilie_model_partner',
#             'objects': http.request.env['reconcilie_model_partner.reconcilie_model_partner'].search([]),
#         })

#     @http.route('/reconcilie_model_partner/reconcilie_model_partner/objects/<model("reconcilie_model_partner.reconcilie_model_partner"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('reconcilie_model_partner.object', {
#             'object': obj
#         })
