# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProductCategory(models.Model):
    _inherit = 'product.category'

    company_id = fields.Many2one('res.company', 'Company')
