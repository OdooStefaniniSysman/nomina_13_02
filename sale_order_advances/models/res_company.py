# -*- coding: utf-8 -*-

from odoo import api, fields, models


class ResCompany(models.Model):
    _inherit = "res.company"
    
    sale_order_advance_required = fields.Boolean(
        'Advance Required'
    )
    sale_order_advance_required_percentage = fields.Float(
        "Percentage of Advance Required for Sales"
    )
