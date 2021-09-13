# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_compare
from datetime import datetime
from collections import defaultdict

MAP_INVOICE_TYPE_PARTNER_TYPE = {
    'out_invoice': 'customer',
    'out_refund': 'customer',
    'out_receipt': 'customer',
    'in_invoice': 'supplier',
    'in_refund': 'supplier',
    'in_receipt': 'supplier',
}
import logging

_logger = logging.getLogger(__name__)


class AccountPayment(models.Model):
    _inherit = 'account.payment'
    
    payment_has_exchange_rate = fields.Boolean('Payment has currency exchange rate')
    payment_exchange_rate = fields.Float('Document Exchange Rate Value', default=1)
    payment_exchange_allow_ok = fields.Boolean('Allow Exchange Rate', compute="_compute_payment_exchange_allow")
    currency_rate = fields.Float(
        "Currency Rate",
        compute='_compute_currency_rate', 
        compute_sudo=True,
        store=True,
        digits=(12, 6),
        readonly=True,
        help='The rate of the currency to the currency of rate 1 applicable at the date of the payment'
    )
    currency_signed_id = fields.Many2one('res.currency', string="Company Currency", related='journal_id.company_id.currency_id', readonly=True)
    amount_signed = fields.Monetary(
        string='Local Currency',
        store=True,
        readonly=True,
        compute='_compute_amount_signed',
        currency_field='currency_signed_id'
    )
    analytic_account_id = fields.Many2one('account.analytic.account',string='Analytic Account',required=False)
    
    @api.model
    def default_get(self, default_fields):
        res = super(AccountPayment, self).default_get(default_fields)
        return res

    @api.onchange('currency_id')
    def _onchange_currency(self):
        res = super(AccountPayment,self)._onchange_currency()
        for invoice in self.invoice_ids:
            if invoice.currency_id.id != self.currency_id.id:
                return {
                    'warning': {
                        'title': _('Payment Currency Warning'),
                        'message': _('The payment currency is different from the currency of any of the related invoices.')
                    }
                }
        return res
 
    @api.depends('currency_id', 'company_id', 'payment_has_exchange_rate','journal_id')
    def _compute_payment_exchange_allow(self):
        self.payment_exchange_allow_ok = False
        if self.currency_id != self.journal_id.company_id.currency_id:
            self.payment_exchange_allow_ok = True
    
    @api.onchange('payment_has_exchange_rate')
    def _onchange_payment_has_exchange_rate(self):
        if not self.payment_has_exchange_rate:
            self.payment_exchange_rate = 1

    @api.depends(
        'journal_id',
        'payment_date',
        'company_id',
        'amount_signed',
        'amount',
        'payment_has_exchange_rate',
        'payment_exchange_rate',
        'currency_id')
    def _compute_amount_signed(self):
        for payment in self:
            amount = payment.amount
            amount_signed = 0.0
            currencies = set()
            company_currency = payment.journal_id.company_id.currency_id or self.env.company.currency_id
            journal_currency = payment.journal_id.currency_id or company_currency
            payment_currency = payment.currency_id or company_currency
            if payment_currency == journal_currency:
                payment_currency.amount_signal = amount
                continue
            if payment.payment_has_exchange_rate and payment.payment_exchange_rate > 1:
                payment.amount_signed = payment_currency._convert_per_document(
                    payment.amount, journal_currency, payment.journal_id.company_id,
                    payment.payment_date or fields.Date.today(),payment.payment_exchange_rate)
            else:
                payment.amount_signed = payment_currency._convert(
                    payment.amount, journal_currency, payment.journal_id.company_id,
                    payment.payment_date or fields.Date.today())
                
    @api.depends('journal_id', 'payment_date', 'company_id','currency_id')
    def _compute_currency_rate(self):
        for payment in self:
            date = self._context.get('date') or datetime.today()
            company_currency = payment.journal_id.company_id.currency_id or self.env.company.currency_id
            journal_currency = payment.journal_id.currency_id or company_currency
            payment_currency = payment.currency_id or company_currency
            currency = payment.currency_id.id
            if payment_currency == journal_currency:
                currency = payment_currency.id
            self.env['res.currency.rate'].flush(['rate', 'currency_id', 'company_id', 'name'])
            query = """SELECT c.id,
                COALESCE((SELECT r.rate FROM res_currency_rate r
                    WHERE r.currency_id = c.id AND r.name <= %s
                    AND (r.company_id IS NULL OR r.company_id = %s)
                    ORDER BY r.company_id, r.name DESC
                    LIMIT 1), 1.0) AS rate
                    FROM res_currency c
                WHERE c.id = %s"""
            company_obj = self.env['res.company'].browse(self.env.company.id)
            self._cr.execute(query, (date, company_obj.id, currency))
            currency_rates = dict(self._cr.fetchall())
            rate = currency_rates.get(currency) or 1.0
            self.currency_rate = 1 / rate if rate > 0 else 1


    def action_register_payment(self):
        res = super(AccountPayment, self).action_register_payment()
        active_ids = self.env.context.get('active_ids')
        if not active_ids:
            return ''
        currency_cont = len(self.env['account.move'].read_group([('id', 'in', active_ids)], fields=['id'], groupby=['currency_id']))
        self.env.context = dict(self.env.context)
        self.env.context.update({'message_many_currencies': False})
        if currency_cont > 1:
            self.env.context.update({'message_many_currencies': True})
        res.update({'context': self.env.context})
        return res
    
    def _prepare_payment_moves(self):
        res = super(AccountPayment, self)._prepare_payment_moves()
        all_move_vals = []
        for payment in self:
            if payment.payment_has_exchange_rate and payment.payment_exchange_rate > 1:
                company_currency = payment.company_id.currency_id
                move_names = payment.move_name.split(payment._get_move_name_transfer_separator()) if payment.move_name else None

                # Compute amounts.
                write_off_amount = payment.payment_difference_handling == 'reconcile' and -payment.payment_difference or 0.0
                if payment.payment_type in ('outbound', 'transfer'):
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
                    balance = payment.currency_id._convert_per_document(
                        counterpart_amount,
                        company_currency,
                        payment.company_id,
                        payment.payment_date,
                        payment.payment_exchange_rate
                    )
                    write_off_balance = payment.currency_id._convert_per_document(
                        write_off_amount,
                        company_currency,
                        payment.company_id,
                        payment.payment_date,
                        payment.payment_exchange_rate
                    )
                    currency_id = payment.currency_id.id

                # Manage custom currency on journal for liquidity line.
                if payment.journal_id.currency_id and payment.currency_id != payment.journal_id.currency_id:
                    # Custom currency on journal.
                    if payment.journal_id.currency_id == company_currency:
                        # Single-currency
                        liquidity_line_currency_id = False
                    else:
                        liquidity_line_currency_id = payment.journal_id.currency_id.id
                    liquidity_amount = company_currency._convert_per_document(
                        balance, payment.journal_id.currency_id, payment.company_id, payment.payment_date, payment.payment_exchange_rate)
                else:
                    # Use the payment currency.
                    liquidity_line_currency_id = currency_id
                    liquidity_amount = counterpart_amount

                # Compute 'name' to be used in receivable/payable line.
                rec_pay_line_name = ''
                if payment.payment_type == 'transfer':
                    rec_pay_line_name = payment.name
                else:
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

                # Compute 'name' to be used in liquidity line.
                if payment.payment_type == 'transfer':
                    liquidity_line_name = _('Transfer to %s') % payment.destination_journal_id.name
                else:
                    liquidity_line_name = payment.name

                # ==== 'inbound' / 'outbound' ====

                move_vals = {
                    'date': payment.payment_date,
                    'ref': payment.communication,
                    'journal_id': payment.journal_id.id,
                    'currency_id': payment.journal_id.currency_id.id or payment.company_id.currency_id.id,
                    'partner_id': payment.partner_id.id,
                    'line_ids': [
                        # Receivable / Payable / Transfer line.
                        (0, 0, {
                            'name': rec_pay_line_name,
                            'amount_currency': counterpart_amount + write_off_amount if currency_id else 0.0,
                            'currency_id': currency_id,
                            'debit': balance + write_off_balance > 0.0 and balance + write_off_balance or 0.0,
                            'credit': balance + write_off_balance < 0.0 and -balance - write_off_balance or 0.0,
                            'date_maturity': payment.payment_date,
                            'partner_id': payment.partner_id.commercial_partner_id.id,
                            'account_id': payment.destination_account_id.id,
                            'payment_id': payment.id,
                            'analytic_account_id': self.analytic_account_id.id if self.analytic_account_id else '',
                        }),
                        # Liquidity line.
                        (0, 0, {
                            'name': liquidity_line_name,
                            'amount_currency': -liquidity_amount if liquidity_line_currency_id else 0.0,
                            'currency_id': liquidity_line_currency_id,
                            'debit': balance < 0.0 and -balance or 0.0,
                            'credit': balance > 0.0 and balance or 0.0,
                            'date_maturity': payment.payment_date,
                            'partner_id': payment.partner_id.commercial_partner_id.id,
                            'account_id': liquidity_line_account.id,
                            'payment_id': payment.id,
                            'analytic_account_id': self.analytic_account_id.id if self.analytic_account_id else '',
                        }),
                    ],
                }
                if write_off_balance:
                    # Write-off line.
                    move_vals['line_ids'].append((0, 0, {
                        'name': payment.writeoff_label,
                        'amount_currency': -write_off_amount,
                        'currency_id': currency_id,
                        'debit': write_off_balance < 0.0 and -write_off_balance or 0.0,
                        'credit': write_off_balance > 0.0 and write_off_balance or 0.0,
                        'date_maturity': payment.payment_date,
                        'partner_id': payment.partner_id.commercial_partner_id.id,
                        'account_id': payment.writeoff_account_id.id,
                        'payment_id': payment.id,
                        'analytic_account_id': self.analytic_account_id.id if self.analytic_account_id else '',
                    }))

                if move_names:
                    move_vals['name'] = move_names[0]

                all_move_vals.append(move_vals)

                # ==== 'transfer' ====
                if payment.payment_type == 'transfer':
                    journal = payment.destination_journal_id

                    # Manage custom currency on journal for liquidity line.
                    if journal.currency_id and payment.currency_id != journal.currency_id:
                        # Custom currency on journal.
                        liquidity_line_currency_id = journal.currency_id.id
                        transfer_amount = company_currency._convert_per_document(
                            balance,
                            journal.currency_id,
                            payment.company_id,
                            payment.payment_date,
                            payment.payment_exchange_rate
                        )
                    else:
                        # Use the payment currency.
                        liquidity_line_currency_id = currency_id
                        transfer_amount = counterpart_amount

                    transfer_move_vals = {
                        'date': payment.payment_date,
                        'ref': payment.communication,
                        'partner_id': payment.partner_id.id,
                        'journal_id': payment.destination_journal_id.id,
                        'line_ids': [
                            # Transfer debit line.
                            (0, 0, {
                                'name': payment.name,
                                'amount_currency': -counterpart_amount if currency_id else 0.0,
                                'currency_id': currency_id,
                                'debit': balance < 0.0 and -balance or 0.0,
                                'credit': balance > 0.0 and balance or 0.0,
                                'date_maturity': payment.payment_date,
                                'partner_id': payment.partner_id.commercial_partner_id.id,
                                'account_id': payment.company_id.transfer_account_id.id,
                                'payment_id': payment.id,
                                'analytic_account_id': self.analytic_account_id if self.analytic_account_id else '',
                            }),
                            # Liquidity credit line.
                            (0, 0, {
                                'name': _('Transfer from %s') % payment.journal_id.name,
                                'amount_currency': transfer_amount if liquidity_line_currency_id else 0.0,
                                'currency_id': liquidity_line_currency_id,
                                'debit': balance > 0.0 and balance or 0.0,
                                'credit': balance < 0.0 and -balance or 0.0,
                                'date_maturity': payment.payment_date,
                                'partner_id': payment.partner_id.commercial_partner_id.id,
                                'account_id': payment.destination_journal_id.default_credit_account_id.id,
                                'payment_id': payment.id,
                                'analytic_account_id': self.analytic_account_id if self.analytic_account_id else '',
                            }),
                        ],
                    }

                    if move_names and len(move_names) == 2:
                        transfer_move_vals['name'] = move_names[1]

                    all_move_vals.append(transfer_move_vals)
                return all_move_vals
            else:
                return res
        
        
class payment_register(models.TransientModel):
    _inherit = 'account.payment.register'

    message_many_currencies = fields.Boolean(string='Message Diferent Currency', compute='_get_context_message_many_currencies')
    
    @api.depends('journal_id')
    def _get_context_message_many_currencies(self):
        self.message_many_currencies = False
        if dict(self.env.context)['message_many_currencies'] == True:
            self.message_many_currencies = True


    @api.model
    def default_get(self, fields):
        rec = super(payment_register, self).default_get(fields)
        active_ids = self._context.get('active_ids')
        if not active_ids:
            return rec
        invoices = self.env['account.move'].browse(active_ids)
        unique_invoice_currency = None
        for invoice in invoices:
            if not unique_invoice_currency:
                unique_invoice_currency = invoice.currency_id
            #if unique_invoice_currency != invoice.currency_id:
            #    raise Warning(_("The payment currency is different from the currency of any of the related invoices"))
        return rec

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
