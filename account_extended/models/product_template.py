# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    concept_type_id = fields.Many2one('product.concept.type', string='Concept Type')