# -*- coding: utf-8 -*-
import xlsxwriter
import io
import base64

from odoo import api, fields, models
from odoo.http import content_disposition

class SupplierVoucherWizard(models.TransientModel):
    _name = 'supplier.voucher.wizard'
    _description = 'Supplier voucher wizard'

    partner_id = fields.Many2one('res.partner', string='Partners')
    move_id = fields.Many2one('account.move', string='Document')
    line_ids = fields.Many2many('account.move.line', string='Lines')
    

    @api.onchange('move_id')
    def _onchange_move_id(self):
        partner_ids = []
        if self.move_id:
            partner_ids = self.move_id.line_ids.mapped('partner_id').ids
        return {'domain': {'partner_id': [('id', 'in', partner_ids)]}}    
    
    @api.onchange('partner_id', 'move_id')
    def _onchange_partner_id(self):
        line_ids = []
        if self.partner_id and self.move_id:
            line_ids = self.move_id.line_ids.filtered(lambda line: line.partner_id.id == self.partner_id.id and line.tax_base_amount == 0.0).ids
            return {
                'domain': {'line_ids': [('id', 'in', line_ids)]},
            }

    def generate_voucher(self):
        print('Hallo')