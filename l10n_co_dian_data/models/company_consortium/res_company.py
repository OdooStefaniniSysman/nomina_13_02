# -*- coding: utf-8 -*-

from odoo import api, fields, models

class ResCompany(models.Model):
    _inherit = 'res.company'

    is_ut = fields.Boolean(string='Es unión temporal?', default=False)
    members_ids = fields.One2many('res.consortium.members', 'consortium_id', string='Members')
    