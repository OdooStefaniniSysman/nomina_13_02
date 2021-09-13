from odoo import models,api,fields,_

import logging

_logger = logging.getLogger(__name__)

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    sync1 = fields.Binary(string='Sync 1')
    sync2 = fields.Binary(string='Sync 2')
    sync3 = fields.Binary(string='Sync 3')
    bool_wizard = fields.Boolean(compute='_compute_bool_wizard')
    
    
    @api.depends('picking_type_id')
    def _compute_bool_wizard(self):
        for record in self:
            if record.picking_type_id.warehouse_id.id == 161:
                record.bool_wizard = True
            elif record.picking_type_id.warehouse_id.id == 156 and record.picking_type_id.name in ['Órdenes de Entrega','Fabricación','Elegir Componentes']:
                record.bool_wizard = True
            else:
                record.bool_wizard = False
                
    def active_wizard_stock(self):
        super(StockPicking,self).action_assign()
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'stock.picking.wizard',
            'view_mode': 'form',
            'views': [(False,  'form')],
            'target': 'new',
        }
    
    
    def _create_backorder(self):
        backorders = self.env['stock.picking']
        for picking in self:
            moves_to_backorder = picking.move_lines.filtered(lambda x: x.state not in ('done', 'cancel'))
            if moves_to_backorder:
                backorder_picking = picking.copy({
                    'name': '/',
                    'move_lines': [],
                    'move_line_ids': [],
                    'backorder_id': picking.id
                })
                picking.message_post(
                    body=_('The backorder <a href=# data-oe-model=stock.picking data-oe-id=%d>%s</a> has been created.') % (
                        backorder_picking.id, backorder_picking.name))
                moves_to_backorder.write({'picking_id': backorder_picking.id})
                moves_to_backorder.mapped('move_line_ids').write({'requested': backorder_picking.id})
                moves_to_backorder.mapped('package_level_id').write({'picking_id':backorder_picking.id})
                moves_to_backorder.mapped('move_line_ids').write({'picking_id': backorder_picking.id})
                backorder_picking.action_assign()
                backorders |= backorder_picking
                
                for move in moves_to_backorder:
                    move.write({'requested': move.product_uom_qty })
                
                _logger.error('************************************************************\n+++++++++++++++++++')
                _logger.error(moves_to_backorder)
        return backorders
