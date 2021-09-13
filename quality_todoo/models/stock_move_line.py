from odoo import models, fields, api, _
from datetime import datetime
from datetime import timedelta
from odoo.exceptions import ValidationError,RedirectWarning

class StockMoveLineThomas(models.Model):
    _inherit = 'stock.move.line'

    quality_id = fields.Many2one('quality.alert')


class StockMoveThomas(models.Model):
    _inherit = 'stock.move'
    team_id = fields.Many2one('quality.alert.team', default="")

    def create_quality_check(self):
        
        dic = []
        for lines in self.move_line_nosuggest_ids:
            vals = {
                'product_id': self.product_id.id,
                'team_id': self.team_id.id,
                #'picking_id': lines.location_des_id.id,
                #'lot_id': lines.lot_name,
            }
        self.env['quality.check'].create(vals)
         


     


        

    
        	