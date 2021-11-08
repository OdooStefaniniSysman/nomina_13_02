# -*- coding: utf-8 -*-

from odoo import models, api, fields, _
from odoo.exceptions import Warning, UserError
import logging

_logger = logging.getLogger(__name__)

class MaterialPurchaseRequisition(models.Model):
    _inherit = 'material.purchase.requisition'

    responsable_area = fields.Char('Responsable Area',compute='_compute_responsable_area')
    charge_to = fields.Selection([('order','Production Order'),('center','Cost Center')],'Charge To')
    production_id = fields.Many2one('mrp.production','Production Order',domain=[('state','not in',('draft','done','cancel'))])
    cost_center_id = fields.Many2one('mrp.workcenter','Cost Center')
    delivery_by = fields.Char('Delivery By',compute="_compute_delivery_by")
    recieved_by = fields.Char('recieved By',compute="_compute_recieve_by")
    security_aux = fields.Char('Security Auxiliar',compute="_compute_security_aux")
    
    
    
    def cargar(self):
        if self.charge_to == 'order':
            if len(self.requisition_line_ids) > 0 and self.production_id:
                list = []
                if self.production_id.bool_state == False:
                    for lines in self.requisition_line_ids:
                        #_logger.error(lines.product_id.uom_id.category_id)
                        #_logger.error(lines.product_id)
                        dic={
                            'name':self.production_id.name,
                            'product_id':lines.product_id.id,
                            'product_uom':lines.product_id.uom_id.id,
                            'location_id':self.production_id.location_src_id.id,
                            'location_dest_id':self.production_id.location_dest_id.id,
                            'product_uom_qty': 1,
                            #'product_qty': 1,
                            'quantity_done': 1,
                             #'reserved_availability': 1,
                            #'move_line_ids': [(0,0,{'qty_done': 12,
                             #                        'product_uom_id':lines.product_id.uom_id.id,
                              #                       'location_id':self.production_id.location_src_id.id,
                               #                      'location_dest_id':self.production_id.location_dest_id.id,
                                #                     'product_id':lines.product_id.id,})]
                                                     #'product_uom_qty': 1,})]
                        }
                        list.append((0,0,dic))
                        production_line_id = self.env['mrp.production'].browse(self.production_id.id)
                        #production_line_ids.action_toggle_is_locked()
                        production_line_id.write({'move_raw_ids':list})
                        #_logger.error("el proceso te termino con exito")
                    message = {

                           'type': 'ir.actions.client',

                           'tag': 'display_notification',

                           'params': {

                               'title': _('Warning!'),

                               'message': 'Productos cargados con exito',

                               'sticky': False, }
                            }
                else:
                    message = {

                           'type': 'ir.actions.client',

                           'tag': 'display_notification',

                           'params': {

                               'title': _('Warning!'),

                               'message': 'No puede cargar productos a una orden bloqueada',

                               'sticky': False, }
                            }
                return message
    
    def _compute_security_aux(self):
        for record in self:
            stock_id = record.env['stock.picking'].search([('origin','=',record.name),('state','in',('assigned','done'))],limit=1)
            if record.state == 'stock' and stock_id:
                record.security_aux = stock_id.security_aux_id.name
            else:
                record.security_aux = ''
    
    def _compute_recieve_by(self):
        for record in self:
            stock_id = record.env['stock.picking'].search([('origin','=',record.name),('state','in',('assigned','done'))],limit=1)
            if record.state == 'stock' and stock_id:
                record.recieved_by = stock_id.recieved_id.name
            else:
                record.recieved_by = ''
    
    def _compute_delivery_by(self):
        for record in self:
            stock_id = record.env['stock.picking'].search([('origin','=',record.name),('state','in',('assigned','done'))],limit=1)
            if record.state == 'stock' and stock_id:
                record.delivery_by = stock_id.delivery_id.name
            else:
                record.delivery_by = ''


    @api.depends('department_id')
    def _compute_responsable_area(self):
        if self.department_id:
            self.responsable_area =  self.department_id.sudo().manager_id.name if self.department_id.sudo().manager_id else ''
        else:
            self.responsable_area = ''
    
    @api.model
    def _prepare_po_line_modify(self, line=False, purchase_order=False):
        po_line_vals = {
                 'product_id': line.product_id.id,
                 'name':line.product_id.name,
                 'product_qty': line.qty,
                 'product_uom': line.uom.id,
                 'date_planned': fields.Date.today(),
                 'price_unit': line.product_id.standard_price,
                 'order_id': purchase_order.id,
                 'account_analytic_id': line.analytic_account_id.id,
                 'custom_requisition_line_id': line.id
        }
        return po_line_vals
            
    @api.model
    def _prepare_pick_vals_modify(self, line=False, stock_id=False):
        pick_vals = {
            'product_id' : line.product_id.id,
            'product_uom_qty' : line.qty,
            'product_uom' : line.uom.id,
            'location_id' : self.location_id.id,
            'location_dest_id' : self.dest_location_id.id,
            'name' : line.product_id.name,
            'picking_type_id' : self.custom_picking_type_id.id,
            'picking_id' : stock_id.id,
            'custom_requisition_line_id' : line.id,
            'company_id' : line.requisition_id.company_id.id,
        }
        return pick_vals

    def request_stock_modify(self):
        stock_obj = self.env['stock.picking']
        move_obj = self.env['stock.move']
        purchase_obj = self.env['purchase.order']
        purchase_line_obj = self.env['purchase.order.line']
        for rec in self:
            if not rec.requisition_line_ids:
                raise Warning(_('Please create some requisition lines.'))
            if any(line.requisition_type =='internal' for line in rec.requisition_line_ids):
                if not rec.location_id.id:
                        raise Warning(_('Select Source location under the picking details.'))
                if not rec.custom_picking_type_id.id:
                        raise Warning(_('Select Picking Type under the picking details.'))
                if not rec.dest_location_id:
                    raise Warning(_('Select Destination location under the picking details.'))
                picking_vals = {
                        'partner_id' : rec.employee_id.sudo().address_home_id.id,
                        'location_id' : rec.location_id.id,
                        'location_dest_id' : rec.dest_location_id and rec.dest_location_id.id or rec.employee_id.dest_location_id.id or rec.employee_id.department_id.dest_location_id.id,
                        'picking_type_id' : rec.custom_picking_type_id.id,#internal_obj.id,
                        'note' : rec.reason,
                        'custom_requisition_id' : rec.id,
                        'origin' : rec.name,
                        'company_id' : rec.company_id.id,
                        
                    }
                stock_id = stock_obj.sudo().create(picking_vals)
                delivery_vals = {
                        'delivery_picking_id' : stock_id.id,
                    }
                rec.write(delivery_vals)
                
            po_dict = {}
            for line in rec.requisition_line_ids:
                if line.requisition_type =='internal':
                    pick_vals = rec._prepare_pick_vals_modify(line, stock_id)
                    move_id = move_obj.sudo().create(pick_vals)
                #else:
                if line.requisition_type == 'purchase': #10/12/2019
                    if not line.partner_id:
                        raise Warning(_('Please enter atleast one vendor on Requisition Lines for Requisition Action Purchase'))
                    for partner in line.partner_id:
                        if partner not in po_dict:
                            po_vals = {
                                'partner_id':partner.id,
                                'currency_id':rec.env.user.company_id.currency_id.id,
                                'date_order':fields.Date.today(),
                                'company_id':rec.company_id.id,
                                'custom_requisition_id':rec.id,
                                'origin': rec.name,
                            }
                            purchase_order = purchase_obj.create(po_vals)
                            po_dict.update({partner:purchase_order})
                            po_line_vals = rec._prepare_po_line_modify(line, purchase_order)
                            purchase_line_obj.sudo().create(po_line_vals)
                        else:
                            purchase_order = po_dict.get(partner)
                            po_line_vals = rec._prepare_po_line_modify(line, purchase_order)
                            purchase_line_obj.sudo().create(po_line_vals)
                rec.state = 'stock'
    
class MaterialPurchaseRequisitionLine(models.Model):
    _inherit = 'material.purchase.requisition.line'

    inspection_state = fields.Char('Inspection State',compute="_compute_inspection_state")
    analytic_account_id = fields.Many2one('account.analytic.account','Cost Center')
    lot = fields.Char('Lots and Serial Number',compute="_compute_lot")
    bool_state = fields.Boolean(compute='_compute_bool_state')
    uom_id = fields.Many2one('uom.uom','Unit of Measure',related='product_id.uom_id')
    
    @api.depends('requisition_id.state')
    def _compute_bool_state(self):
        for record in self:
            if record.requisition_id.state != 'draft':
                record.bool_state = True
            else:
                record.bool_state = False
            
    
    @api.onchange('analytic_account_id')
    def _onchange_analytic_account_id(self):
        for record in self:
            if record.requisition_id.charge_to == 'order' and record.analytic_account_id:
                raise UserError(_('Do not charge to production order and select cost center'))
    
    @api.depends('product_id')
    def _compute_inspection_state(self):
        picking = []
        for record in self:
            if record.requisition_id.state == 'receive' and record.requisition_type == 'internal':
                picking_id = record.env['stock.move'].search([('product_id','=',record.product_id.id),('picking_id.custom_requisition_id','=',record.requisition_id.id)])
                for stock in picking_id:
                    if picking_id and record.requisition_type == 'internal':
                        picking.append(stock.inspection_state)
                        for x in range(len(picking)):
                            record.inspection_state = picking[x]
                    else:
                        record.inspection_state = ''
            else:
                record.inspection_state = ''
                    
    @api.depends('product_id')
    def _compute_lot(self):
        picking = []
        for record in self:
            if record.requisition_id.state == 'receive' and record.requisition_type == 'internal':
                picking_id = record.env['stock.move.line'].search([('product_id','=',record.product_id.id),('picking_id.custom_requisition_id','=',record.requisition_id.id)])
                for stock in picking_id:
                    if picking_id:
                        picking.append(stock.lot_id.name)
                        for x in range(len(picking)):
                            record.lot = picking[x]
                    else:
                        record.lot = ''
            else:
                record.lot = ''
                
    @api.onchange('qty')
    def _onchange_qty(self):
        for record in self:
            if record.qty < 1:
                raise UserError(_('Do not Use negative values'))
                




