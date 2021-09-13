# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResPartner(models.Model):
    _name = 'res.partner.alternative.person'

    name = fields.Char(string='name')
    partner_id = fields.Many2one('res.partner', string='Customer')

    