# -*- coding: utf-8 -*-

from odoo import models, api, fields, _
from odoo.exceptions import Warning, UserError
import logging

_logger = logging.getLogger(__name__)

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    charge_to = fields.Selection([('order','Production Order'),('center','Cost Center')],'Charge To')
    production_id = fields.Many2one('mrp.production','Production Order', domain=[('state','not in',('draft','done','cancel'))])

    purchase_type = fields.Selection(
        string="Purchase type",
        selection=[
                ('national', 'National'),
                ('import', 'Import'),
        ],
    )
    date_end = fields.Date(string="Fecha Limite")

    @api.onchange('order_line')
    def _onchange_order_line(self):
        if self.order_line:
            c = 1
            for line in self.order_line:
                if line.item == 0:
                    line.item = c
                c += 1

    def go_to_requisition(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Requisición'),
            'res_model': 'material.purchase.requisition',
            'view_mode': 'tree,form','domain': [('id', '=', self.custom_requisition_id.id)],
		}


        
class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    item = fields.Integer(string='Item')
    isnt_draft = fields.Boolean(string='state auxiliar', compute='_compute_isnt_draft')

    @api.depends('order_id.state')
    def _compute_isnt_draft(self):
        for record in self:
            if record.order_id.state != 'draft':
                record.isnt_draft = True
            else:
                record.isnt_draft = False


    def _prepare_account_move_line(self, move):
        vals = super(PurchaseOrderLine,self)._prepare_account_move_line(move)
        vals["item"] = self.item
        return vals