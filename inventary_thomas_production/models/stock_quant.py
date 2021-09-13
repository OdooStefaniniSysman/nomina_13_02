from odoo import _, api, fields, models

class StockQuant(models.Model):
    _inherit = 'stock.quant'

    production_id = fields.Many2one('mrp.production','Production Order',compute="_compute_production_id")
    
    @api.depends('lot_id')
    def _compute_production_id(self):
        for record in self:
            production_id = record.env['mrp.production'].search([('location_dest_id','=',record.location_id.id),('product_id','=',record.product_id.id)],limit=1)
            if production_id:
                record.production_id = production_id.id
            else:
                record.production_id = ''
