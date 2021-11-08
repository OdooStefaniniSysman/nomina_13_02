from odoo import models, fields, api, _
from datetime import datetime
from datetime import timedelta
from odoo.exceptions import ValidationError,RedirectWarning

class StockMoveLineThomas(models.Model):
    _inherit = 'stock.move.line'

    quality_id = fields.Many2one('quality.alert')


    def create_record_quality(self):
        vals = {
         'name': self.lot_name,
        }
        self.env['quality.alert'].create(vals)

    
    def write(self, vals):
        if vals.get('lot_name'):
	        if vals.get('lot_name') != 'False':
	            lines_dict = {
	                'product_id': self.id,
	               
	            }
	            self.env['quality.alert'].create(lines_dict)
	            return super(StockMoveLineThomas, self).write(vals)    

    
        	