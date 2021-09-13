# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    #alternative_contact = fields.Many2one('res.partner.alternative.person', string='Alternative Contact')
    property_alternative_contact_id = fields.Many2one('res.partner.alternative.person', company_dependent=True,
        string="Alternative Contact",
        required=False)
