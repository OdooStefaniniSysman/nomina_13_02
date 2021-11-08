from odoo import models, fields, api

class Todoo(models.Model):
    _inherit = 'sale.order.line'

    porcent=fields.Integer(string="Margen")
    margen=fields.Integer(related="total_margen", string="%")
    total_margen = fields.Integer(string="Margen")
    

    @api.depends('purchase_price','price_unit')
    def _compute_margen(self):
        for record in self:
            record.total_margen = (int(record.price_unit)  - int(record.purchase_price)) / 1000

