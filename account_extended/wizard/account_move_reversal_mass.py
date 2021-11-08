# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.tools.translate import _
from odoo.exceptions import RedirectWarning, UserError, ValidationError


class AccountMoveReversalMass(models.TransientModel):
    _name = 'account.move.reversal.mass'
    _description = 'Account Move Reversal Massive'

    move_id = fields.Many2one('account.move', string='Journal Entry',
        domain=[('state', '=', 'posted'), ('type', 'not in', ('out_refund', 'in_refund'))])
    date = fields.Date(string='Reversal date', default=fields.Date.context_today, required=True)
    reason = fields.Char(string='Reason')
    refund_method = fields.Selection(selection=[
            ('refund', 'Partial Refund'),
            ('cancel', 'Full Refund'),
            ('modify', 'Full refund and new draft invoice')
        ], string='Credit Method', required=True, default='modify')
    journal_id = fields.Many2one('account.journal', string='Use Specific Journal', help='If empty, uses the journal of the journal entry to be reversed.')
    journal_new_id = fields.Many2one('account.journal', string='Journal for new invoice', help='If it is empty, use the original journal entry to create the new one.')
    discrepancy_response_code_id = fields.Many2one(
        comodel_name='account.invoice.discrepancy.response.code',
        string='Correction concept for Refund Invoice')


    @api.onchange('discrepancy_response_code_id')
    def _onchange_discrepancy_response_code_id(self):
        if self.discrepancy_response_code_id:
            self.reason = self.discrepancy_response_code_id.name


    def reverse_moves(self):
        self.ensure_one()
        active_ids = self._context.get('active_ids')
        invoices = self.env['account.move'].browse(active_ids)

        if any(type != 'out_invoice' for type in invoices.mapped('type')):
            raise UserError(_("Sorry!. This wizard can only be used with customer invoices."))

        if any(state != 'posted' for state in invoices.mapped('state')):
            raise UserError(_("Sorry!. This wizard can only be used with customer invoices in post state."))

        reverse = self.env['account.move.reversal']
        vals = {
            'date': self.date,
            'reason': self.reason,
            'refund_method': self.refund_method or 'modify',
            'journal_id': self.journal_id and self.journal_id.id or False,
            'journal_new_id': self.journal_new_id and self.journal_new_id.id or False,
            'discrepancy_response_code_id': self.discrepancy_response_code_id.id,
        }
        reverse_wizard = reverse.with_context(refund_type='credit').create(vals)
        reverse_wizard.reverse_moves()


class AccountMoveReversal(models.TransientModel):
    _inherit = 'account.move.reversal'


    journal_new_id = fields.Many2one('account.journal', string='Journal for new invoice', help='If it is empty, use the original journal entry to create the new one.')


    def reverse_moves(self):
        moves = self.env['account.move'].browse(self.env.context['active_ids']) if self.env.context.get('active_model') == 'account.move' else self.move_id

        # Create default values.
        default_values_list = []
        for move in moves:
            refund_type = False
            if move.type and move.type in ('out_invoice','out_refund'):
                refund_type = 'credit'
            elif move.type and move.type == 'in_invoice':
                refund_type = 'debit'

            default_values_list.append({
                'ref': _('Reversal of: %s, %s') % (move.name, self.reason) if self.reason else _('Reversal of: %s') % (move.name),
                'date': self.date or move.date,
                'invoice_date': move.is_invoice(include_receipts=True) and (self.date or move.date) or False,
                'journal_id': self.journal_id and self.journal_id.id or move.journal_id.id,
                'invoice_payment_term_id': None,
                'auto_post': True if self.date > fields.Date.context_today(self) else False,
                'refund_type': refund_type,
            })

        # Handle reverse method.
        if self.refund_method == 'cancel':
            if any([vals.get('auto_post', False) for vals in default_values_list]):
                new_moves = moves._reverse_moves(default_values_list)
            else:
                new_moves = moves._reverse_moves(default_values_list, cancel=True)
        elif self.refund_method == 'modify':
            moves._reverse_moves(default_values_list, cancel=True)
            moves_vals_list = []
            for move in moves.with_context(include_business_fields=True):
                moves_vals_list.append(move.copy_data({
                    'invoice_payment_ref': move.name,
                    'date': self.date or move.date,
                    'journal_id': self.journal_new_id and self.journal_new_id.id or move.journal_id.id,
                })[0])
            new_moves = self.env['account.move'].create(moves_vals_list)
        elif self.refund_method == 'refund':
            new_moves = moves._reverse_moves(default_values_list)
        else:
            return

        # Create action.
        action = {
            'name': _('Reverse Moves'),
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
        }
        if len(new_moves) == 1:
            action.update({
                'view_mode': 'form',
                'res_id': new_moves.id,
            })
        else:
            action.update({
                'view_mode': 'tree,form',
                'domain': [('id', 'in', new_moves.ids)],
            })
        return action


#