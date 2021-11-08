# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.tools import float_is_zero, float_compare, safe_eval, date_utils
from odoo.exceptions import RedirectWarning, UserError, ValidationError, AccessError

import json
import re
import logging

_logger = logging.getLogger(__name__)


class AccountMove(models.Model):
    _inherit = "account.move"
    
    invoice_has_unassigned_advances = fields.Boolean(
        compute = '_compute_invoice_has_unassigned_advances', 
        string = 'Assign Button Control'
    )
    
    advance_payment_ids = fields.One2many(
        comodel_name='account.payment',
		inverse_name='move_id',
		string='Payment Advances',
    )
    
    @api.depends('state')
    def _compute_invoice_has_unassigned_advances(self):
        ''' Implemented control to button invisible  attribute '''
        for rec in self:
            if rec.type not in ['in_receipt','out_receipt','entry']:
                domain = [
                    ('advance_assigned_ok', '=', False),
                    ('state', '=', 'posted'),
                    ('partner_id', '=', rec.partner_id.id),
                ]
                # fixme refund process
                if rec.type in ['out_invoice','in_refund']:
                    domain.append(('payment_type', '=', 'inbound'))
                    domain.append(('partner_type', '=', 'customer'))
                elif rec.type in ['in_invoice','out_refund']:
                    domain.append(('payment_type', '=', 'outbound'))
                    domain.append(('partner_type', '=', 'supplier'))
                advances_ids = self.env['account.payment'].search(domain)
                if advances_ids:
                    rec.invoice_has_unassigned_advances = True
                else:
                    rec.invoice_has_unassigned_advances = False
            else:
                rec.invoice_has_unassigned_advances = False
                    
    @api.constrains('line_ids', 'journal_id')
    def _validate_move_modification(self):
        
        super(AccountMove, self)._validate_move_modification()
        
    def action_assign_advances(self):
        ''' Assign wizard for conciled payment advance '''
        return {
            'name': _('Advance Assign'),
            'view_mode': 'form',
            'res_model': 'wizard.account.invoice.assign.advance',
            'type': 'ir.actions.act_window',
            'context': {'current_id': self.id},
            'target': 'new'
        }


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: