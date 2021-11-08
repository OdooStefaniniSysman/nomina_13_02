# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from datetime import datetime, timedelta
from odoo.exceptions import UserError, ValidationError, Warning

import logging

_logger = logging.getLogger(__name__)


class WizardAccountInvoiceAssignAdvance(models.TransientModel):
    _name = 'wizard.account.invoice.assign.advance'
    _description = 'Wizard for assign advance to invoice'
    
    invoice_id = fields.Many2one('account.move', string='Invoice Number', domain=[],required=True, readonly=True)
    journal_id = fields.Many2one('account.journal', string='Advance Journal', domain=[],required=True)
    currency_id = fields.Many2one('res.currency', string="Company Currency", related='journal_id.company_id.currency_id', readonly=True)
    date = fields.Date('Advance Date',required=True, default=datetime.today())
    amount_total = fields.Monetary(string='Total Invoice Residual', readonly=True)
    amount_total_advances = fields.Monetary(string='Total Unassigned Advances', readonly=True)
    amount_total_assigned = fields.Monetary(string='Total Allocated Advances', readonly=True)
    partner_id = fields.Many2one('res.partner',string='Partner', readonly=True)
    advance_ids = fields.One2many(
		comodel_name='wizard.account.invoice.assign.advance.payment',
		inverse_name='wizard_id',
		string='Allocated Advances',
		required=True,
	)
    
    
    @api.model
    def default_get(self, fields):
        context = dict(self._context or {})
        active_model = context.get('active_model')
        active_ids = context.get('active_ids')
        invoice_id = self.env[active_model].browse(active_ids)
        if invoice_id.type not in ['in_receipt','out_receipt','entry']:
            domain = [
                ('advance_assigned_ok', '=', False),
                ('state', '=', 'posted'),
                ('partner_id', '=', invoice_id.partner_id.id),
                ('payment_as_advance', '=', True),
            ]
            # fixme: refund process
            if invoice_id.type in ['out_invoice','in_refund']:
                domain.append(('payment_type', '=', 'inbound'))
                domain.append(('partner_type', '=', 'customer'))
            elif invoice_id.type in ['in_invoice','out_refund']:
                domain.append(('payment_type', '=', 'outbound'))
                domain.append(('partner_type', '=', 'supplier'))
            advances_ids = self.env['account.payment'].search(domain)
            total_advances = sum(
                advance.amount 
                for advance in advances_ids
            )
            advance_list = []
            for advance in advances_ids:
                advance_list.append((0,0,{
                    'payment_id' : advance.id,
                    'amount' : advance.amount,
                    'journal_id' : advance.journal_id.id,
                    'payment_date' : advance.payment_date,
                    'name': advance.name,
                    }))
        rec = {}
        rec.update({'advance_ids':advance_list})
        rec.update({
            'invoice_id': invoice_id.id,
            'partner_id': invoice_id.partner_id.id,
            'amount_total': invoice_id.amount_residual,
            'amount_total_advances': total_advances,
		})
        return rec
    
    
    
    def register_assign_advances(self):
        for rec in self:
            if not rec.advance_ids.filtered(lambda line: line.assign_ok == True):
                raise UserError(_("No advance has been selected."))
            all_move_vals = []
            for pay in rec.advance_ids.filtered(lambda line: line.assign_ok == True):
                payment = self.env['account.payment'].browse(pay.payment_id)
                AccountMove = self.env['account.move'].with_context(default_type='entry')
                if payment.state != 'posted':
                    raise UserError(_("Only a posted advance payment can be assigned."))
                if self.invoice_id.state != 'posted':
                    raise ValidationError(_("The advance payment cannot be processed because the invoice is not open!"))
                
                company_currency = payment.company_id.currency_id
                # Compute amounts.
                write_off_amount = payment.payment_difference_handling == 'reconcile' and -payment.payment_difference or 0.0
                if payment.payment_type in ('outbound'):
                    counterpart_amount = payment.amount
                    liquidity_line_account = payment.journal_id.default_debit_account_id
                else:
                    counterpart_amount = -payment.amount
                    liquidity_line_account = payment.journal_id.default_credit_account_id

                # Manage currency.
                if payment.currency_id == company_currency:
                    # Single-currency.
                    balance = counterpart_amount
                    write_off_balance = write_off_amount
                    counterpart_amount = write_off_amount = 0.0
                    currency_id = False
                else:
                    # Multi-currencies.
                    balance = payment.currency_id._convert(counterpart_amount, company_currency, payment.company_id, payment.payment_date)
                    write_off_balance = payment.currency_id._convert(write_off_amount, company_currency, payment.company_id, payment.payment_date)
                    currency_id = payment.currency_id.id
                    
                # Manage custom currency on journal for liquidity line.
                if payment.journal_id.currency_id and payment.currency_id != payment.journal_id.currency_id:
                    # Custom currency on journal.
                    if payment.journal_id.currency_id == company_currency:
                        # Single-currency
                        liquidity_line_currency_id = False
                    else:
                        liquidity_line_currency_id = payment.journal_id.currency_id.id
                    liquidity_amount = company_currency._convert(
                        balance, payment.journal_id.currency_id, payment.company_id, payment.payment_date)
                else:
                    # Use the payment currency.
                    liquidity_line_currency_id = currency_id
                    liquidity_amount = counterpart_amount
                    
                # Compute 'name' to be used in receivable/payable line.
                rec_pay_line_name = ''
                if payment.partner_type == 'customer':
                    if payment.payment_type == 'inbound':
                        rec_pay_line_name += _("Customer Payment")
                    elif payment.payment_type == 'outbound':
                        rec_pay_line_name += _("Customer Credit Note")
                elif payment.partner_type == 'supplier':
                    if payment.payment_type == 'inbound':
                        rec_pay_line_name += _("Vendor Credit Note")
                    elif payment.payment_type == 'outbound':
                        rec_pay_line_name += _("Vendor Payment")
                if payment.invoice_ids:
                    rec_pay_line_name += ': %s' % ', '.join(payment.invoice_ids.mapped('name'))

                liquidity_line_name = payment.name

                move_vals = {
                    'date': rec.date,
                    'ref': str(payment.name) + '::Cruce de Anticipo',
                    'journal_id': payment.journal_id.id,
                    'currency_id': payment.journal_id.currency_id.id or payment.company_id.currency_id.id,
                    'partner_id': payment.partner_id.id,
                    'line_ids': [
                        # Receivable / Payable.
                        (0, 0, {
                            'name': str(rec_pay_line_name) + '::Cruce de Anticipo',
                            'amount_currency': counterpart_amount + write_off_amount if currency_id else 0.0,
                            'currency_id': currency_id,
                            'debit': balance + write_off_balance > 0.0 and balance + write_off_balance or 0.0,
                            'credit': balance + write_off_balance < 0.0 and -balance - write_off_balance or 0.0,
                            'date_maturity': rec.date,
                            'partner_id': payment.partner_id.commercial_partner_id.id,
                            'account_id': rec.invoice_id.line_ids\
                            .filtered(lambda move: move.account_id.user_type_id.type in ('receivable', 'payable')).account_id.id,
                            #'payment_id': payment.id,
                        }),
                        # Liquidity line.
                        (0, 0, {
                            'name': str(rec_pay_line_name) + '::Cruce de Anticipo',
                            'amount_currency': -liquidity_amount if liquidity_line_currency_id else 0.0,
                            'currency_id': liquidity_line_currency_id,
                            'debit': balance < 0.0 and -balance or 0.0,
                            'credit': balance > 0.0 and balance or 0.0,
                            'date_maturity': rec.date,
                            'partner_id': payment.partner_id.commercial_partner_id.id,
                            'account_id': payment.destination_account_id.id,
                            #'payment_id': payment.id,
                        }),
                    ],
                }
                if write_off_balance:
                    # Write-off line.
                    move_vals['line_ids'].append((0, 0, {
                        'name': liquidity_line_name,
                        'amount_currency': -write_off_amount,
                        'currency_id': currency_id,
                        'debit': write_off_balance < 0.0 and -write_off_balance or 0.0,
                        'credit': write_off_balance > 0.0 and write_off_balance or 0.0,
                        'date_maturity': payment.payment_date,
                        'partner_id': payment.partner_id.commercial_partner_id.id,
                        'account_id': payment.writeoff_account_id.id,
                        #'payment_id': payment.id,
                    }))

                all_move_vals.append(move_vals)
                moves = AccountMove.create(all_move_vals)
                moves.filtered(lambda move: move.journal_id.post_at != 'bank_rec').post()

                # Update the state / move before performing any reconciliation.
                move_name = moves.mapped('name')
                move_id = moves.mapped('id')
                # finally the payment advance is marked as assigned and hook payment to account.move
                payment.write({
                    'advance_assigned_ok': True,
                    'move_id': rec.invoice_id.id,
                    'move_name': move_name
                })
                
                if payment.payment_type in ('inbound', 'outbound'):
                    if rec.invoice_id:
                        invoice_account_id = rec.invoice_id.line_ids.filtered(
                            lambda move: move.account_id.user_type_id.type in ('receivable', 'payable')
                        ).account_id
                        (
                            (moves[0] + rec.invoice_id).line_ids.filtered(
                                lambda line: not line.reconciled 
                                and line.account_id == payment.destination_account_id 
                                and line.account_id.user_type_id.type in ('receivable', 'payable')
                            )
                            + 
                            (
                                payment.move_line_ids.filtered(
                                    lambda line: not line.reconciled 
                                    and line.account_id == payment.destination_account_id 
                                    and line.account_id.user_type_id.type in ('receivable', 'payable')
                                )
                            )
                        ).reconcile()
                        (
                            (moves[0] + rec.invoice_id).line_ids.filtered(
                                lambda line: not line.reconciled 
                                and line.account_id == invoice_account_id 
                                and line.account_id.user_type_id.type in ('receivable', 'payable')
                            ) 
                            + 
                            (
                                payment.move_line_ids.filtered(
                                    lambda line: not line.reconciled 
                                    and line.account_id == invoice_account_id 
                                    and line.account_id.user_type_id.type in ('receivable', 'payable')
                                )
                            )
                        ).reconcile()

        return True
        

class WizardAccountInvoiceAssignAdvancePayment(models.TransientModel):
    _name = 'wizard.account.invoice.assign.advance.payment'

    wizard_id = fields.Many2one('wizard.account.invoice.assign.advance', string='Assign Advance Form')
    payment_id = fields.Integer(string="Payment ID")
    amount = fields.Float("Payment Amount", required=False)
    journal_id = fields.Many2one('account.journal',string='Journal')
    currency_id = fields.Many2one('res.currency', string="Company Currency", related='journal_id.company_id.currency_id', readonly=True)
    payment_account_id = fields.Many2one('account.account',string='Account')
    payment_date = fields.Date('Date')
    name = fields.Char(string='Payment Number')
    assign_ok = fields.Boolean('Marked Advance')

    @api.onchange('assign_ok')
    def _onchange_assign_ok(self):
        _logger.error('*******************************\n++++++++++++++++++++++++++++++++')
        total_advances = sum(
            advance.amount 
            for advance in self.wizard_id.advance_ids.filtered(lambda line: line.assign_ok == True)
            #if advance.assign_ok = True 
        )
        _logger.error(total_advances)
        self.wizard_id.amount_total_assigned = total_advances
    
    
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4