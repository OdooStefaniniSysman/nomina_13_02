# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_replacement = fields.Boolean(string='is replacement?')
    product_template_id = fields.Many2one('product.template', string='Product replacement')
    
    

class ProductProduct(models.Model):
    _inherit = 'product.product'

    is_replacement = fields.Boolean(string="is replacement?", related='product_tmpl_id.is_replacement')


class StockMove(models.Model):
    _inherit = 'stock.move'

    is_replacement = fields.Boolean(string="¿Es un repuesto?", related='product_id.is_replacement')