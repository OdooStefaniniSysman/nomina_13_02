# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class ProductProduct(models.Model):
    _inherit = 'product.product'
    
    is_tracking_papper_api = fields.Boolean('For tracking papper api')
    