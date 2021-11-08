from odoo import models,api,fields,_
import re
from odoo.exceptions import ValidationError

class StockMoveThomas(models.Model):
    _inherit = 'stock.move'
   
    requested = fields.Float(string="Solicitado")

    @api.constrains('requested')
    def _validate_product_uom_qty(self):
        for record in self:
            if record.requested > record.product_uom_qty:
                raise ValidationError("La Cantidad Solicitada  no puede ser Mayor a la cantidad demandada  : %s" % record.product_uom_qty)



class StockMoveLineThomas(models.Model):
    _inherit = 'stock.move.line'
   
    requested = fields.Float(string="Solicitado", related="move_id.requested")    