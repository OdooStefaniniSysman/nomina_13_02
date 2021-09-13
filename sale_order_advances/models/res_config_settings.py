# -*- coding: utf-8 -*-

from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    
    advance_required = fields.Boolean(
        related = "company_id.sale_order_advance_required",
        string = 'Advance Required',
        readonly=False,
    )
    
    advance_required_percentage = fields.Float(
        related = "company_id.sale_order_advance_required_percentage",
        string = "Percentage of Advance Required for Sales",
        readonly=False,
    )
    