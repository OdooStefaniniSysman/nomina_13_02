from odoo import models,api,fields,_

class StockPickingWizard(models.TransientModel):
    _name = "stock.picking.wizard"
    _description = 'Stock picking wizard'

    sync1 = fields.Binary(string='Sync 1',required=True,store=True)
    sync2 = fields.Binary(string='Sync 2',required=True,store=True)
    sync3 = fields.Binary(string='Sync 3',required=True,store=True)

    def active_validation(self):
        stock_id = self.env['stock.picking'].browse(self._context.get('active_id'))
        stock_id.write({
          'sync1': self.sync1,
          'sync2': self.sync2,
          'sync3': self.sync3,
          #'location_id': stock_id.location_id.id,
          #'location_dest_id': stock_id.location_dest_id.id,
          #'picking_type_id': stock_id.picking_type_id.id,
        })
        return stock_id.button_validate()