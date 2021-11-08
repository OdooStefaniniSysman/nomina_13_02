# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class MrpVariationLine(models.Model):
    _name = 'mrp.variation.line'
    _description = 'Detalle de Variacion en costos de las ordenes de trabajo'

    variation_id = fields.Many2one('mrp.variation', 'Documento de Variaciones')
    
    workorder_id = fields.Many2one('mrp.workorder', 'Orden de Trabajo')
    production_id = fields.Many2one('mrp.production', 'Orden de Fabricación')
    product_id = fields.Many2one('product.product', 'Producto')    
    qty_planned = fields.Float('Cantidad Planificada', digits='Product Unit of Measure')  
    qty_finished = fields.Float('Cantidad Producida',digits='Product Unit of Measure')
    state = fields.Selection([('pending', 'Waiting for another WO'),
                              ('ready', 'Ready'),
                              ('progress', 'In Progress'),
                              ('done', 'Finished'),
                              ('cancel', 'Cancelled')], string='Estado')
    mod_standard = fields.Float('Mod/h Estándar',digits='Product Price')
    cif_standard = fields.Float('Cif/h Estándar',digits='Product Price')
    maq_standard = fields.Float('Maq/h Estándar',digits='Product Price')
    mod_real = fields.Float('Mod/h Real',digits='Product Price')
    cif_real = fields.Float('Cif/h Real',digits='Product Price')
    maq_real = fields.Float('Maq/h Real',digits='Product Price')
    mod_variation = fields.Float('Mod/h Variación',digits='Product Price')
    cif_variation = fields.Float('Cif/h Variación',digits='Product Price')
    maq_variation = fields.Float('Maq/h Variación',digits='Product Price')
    

    
    
    

