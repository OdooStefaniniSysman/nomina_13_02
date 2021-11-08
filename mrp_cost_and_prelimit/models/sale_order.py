# -*- coding: utf-8 -*-
from odoo import models,fields,api,_
import logging

_logger = logging.getLogger(__name__)

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    manufacture_id = fields.Many2one('mrp.production',store=True)
    
    
class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    
    standard_price = fields.Float('Cost',compute='_compute_standard_price',store=True)
    
    @api.depends('product_id')
    def _compute_standard_price(self):
        for record in self:
            if record.product_id:
                record.standard_price = record.product_id.standard_price
            else:
                record.standard_price = 0
                
                
class MrpProduction(models.Model):
    _inherit = 'mrp.production'
    
    @api.model
    def create(self,values):
        _logger.error('este logger +++++++++++++++++++++++++++++++++++++++++++++++++')
        res = super(MrpProduction,self).create(values)
        _logger.error(res)
        if res.origin:
            _logger.error('values--------------------------------------')
            sale_obj = self.env['sale.order'].search([('name','=',res.origin)])
            sale_obj.manufacture_id = res.id
            _logger.error('este logger imprime los vals de mrp produccion')
            _logger.error(values)
        return res