from odoo import fields,api,models

class StockMoveLine(models.Model):
    _inherit = 'stock.move'

    inspection_state = fields.Selection([('according','According'),('released','Released'),('inspection','Without Inspection')],'Inspection State')