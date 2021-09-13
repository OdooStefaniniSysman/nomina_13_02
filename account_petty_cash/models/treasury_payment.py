# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from odoo.tools import float_is_zero, float_compare
from datetime import datetime
from odoo.exceptions import UserError, ValidationError
import logging

_logger = logging.getLogger(__name__)


class TreasuryPayment(models.Model):
    _name = 'treasury.payment'
    _description = 'Petty cash payment for simple account move generation'
    
    name = fields.Char(readonly=True, copy=False)
    payment_reference = fields.Char(string="Referencia del Pago", copy=False, readonly=True)
    payment_date = fields.Date(string='Fecha', default=fields.Date.context_today, 
                               required=True, readonly=True, states={'draft': [('readonly', False)]}, copy=False, tracking=True)
    move_id = fields.Many2one('account.move', string='Asiento Contable', readonly=True)
    state = fields.Selection([('draft', 'Draft'), ('posted', 'Validated'), ('cancelled', 'Cancelled')], readonly=True, default='draft', copy=False, string="Estado")
    amount = fields.Monetary(string='Amount', required=True, readonly=True, states={'draft': [('readonly', False)]}, tracking=True)
    partner_id = fields.Many2one('res.partner', 
                                 string='Tercero', tracking=True, readonly=True, 
                                 states={'draft': [('readonly', False)]}, domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]")
    payment_type = fields.Selection([
            ('outbound', 'Salidas'),
            ('inbound', 'Entradas'), 
            ('infunding', 'Aumento de Fondos'),
            ('outfunding', 'Disminución de Fondos')
        ], string='Tipo de Transacción', required=True, readonly=True, states={'draft': [('readonly', False)]}
    )
    session_id = fields.Many2one(
        'treasury.session', 
        string='Sesión', 
        required=False, 
        index=True,
        domain="[('state', '=', 'posted')]", 
        #states={'draft': [('readonly', False)]},
        readonly=True)
    config_id = fields.Many2one('treasury.config', related='session_id.config_id', string="Caja Menor", readonly=True)
    payment_method_id = fields.Many2one('treasury.payment.method', string="Metodo de Pago")
    journal_id = fields.Many2one('account.journal',related='payment_method_id.cash_journal_id', readonly=True)
    company_id = fields.Many2one('res.company', related='journal_id.company_id', string='Company', readonly=True)
    currency_id = fields.Many2one('res.currency', related='journal_id.currency_id', string='Moneda', readonly=True)
    validate_treasury_ok = fields.Boolean('Validado por Tesorería')
    validate_consignation_ok = fields.Boolean('Consignación')
    consignment_file = fields.Binary(
        string='Adjunto',
    )
    account_id = fields.Many2one('account.account','Cuenta Afectada', 
                                 help='Esta cuenta será la contrapartida de la cuenta del diario que se ha seleccionado a partir del metodo de pago')
    account_analytic_id = fields.Many2one('account.analytic.account','Cuenta Analítica', 
                                 help='Cuenta analítica que será llevada a la linea de los asientos')
    move_line_ids = fields.One2many('account.move.line', 'treasury_payment_id', readonly=True, copy=False, ondelete='restrict')
    
    
    def _prepare_payment_moves(self):
        all_move_vals = []
        for payment in self:
            company_currency = payment.company_id.currency_id
            
            if self.env.company.currency_id == payment.company_id.currency_id:
                counterpart_amount = write_off_amount = 0.0
                balance = counterpart_amount
                write_off_balance = write_off_amount
                currency_id = False
            else:
                raise UserError(_("El módulo de cajas menores no soporte transacciones en una moneda diferente a la moneda de la compañía actual."))

            rec_pay_line_name = ''
            
            if payment.payment_type == 'inbound':
                rec_pay_line_name += _("Entrada Caja Menor")
                debit_line = {
                    'name': rec_pay_line_name,
                    'amount_currency': 0.0,
                    'currency_id': currency_id,
                    'debit': payment.amount,
                    'credit': 0,
                    'date_maturity': payment.payment_date,
                    'partner_id': payment.partner_id.commercial_partner_id.id,
                    'account_id': payment.journal_id.default_debit_account_id.id,
                    'company_id': self.env.company.id,
                    'treasury_payment_id': payment.id,
                }
                credit_line = {
                    'name': rec_pay_line_name,
                    'amount_currency': 0.0,
                    'currency_id': currency_id,
                    'debit': 0.0,
                    'credit': payment.amount,
                    'date_maturity': payment.payment_date,
                    'partner_id': payment.partner_id.commercial_partner_id.id,
                    'account_id': payment.account_id.id,
                    'company_id': self.env.company.id,
                    'treasury_payment_id': payment.id,
                }
            elif payment.payment_type == 'outbound':
                rec_pay_line_name += _("Salida Caja Menor")
                debit_line = {
                    'name': rec_pay_line_name,
                    'amount_currency': 0.0,
                    'currency_id': currency_id,
                    'debit': 0.0,
                    'credit': payment.amount,
                    'date_maturity': payment.payment_date,
                    'partner_id': payment.partner_id.commercial_partner_id.id,
                    'account_id': payment.journal_id.default_credit_account_id.id,
                    'company_id': self.env.company.id,
                    'treasury_payment_id': payment.id,
                }
                credit_line = {
                    'name': rec_pay_line_name,
                    'amount_currency': 0.0,
                    'currency_id': currency_id,
                    'debit': payment.amount,
                    'credit': 0.0,
                    'date_maturity': payment.payment_date,
                    'partner_id': payment.partner_id.commercial_partner_id.id,
                    'account_id': payment.account_id.id,
                    'company_id': self.env.company.id,
                    'treasury_payment_id': payment.id,
                }
            elif payment.payment_type == 'infunding':
                rec_pay_line_name += _("Aumento de Fondos")
                debit_line = {
                    'name': rec_pay_line_name,
                    'amount_currency': 0.0,
                    'currency_id': currency_id,
                    'debit': payment.amount,
                    'credit': 0.0,
                    'date_maturity': payment.payment_date,
                    'partner_id': payment.partner_id.commercial_partner_id.id,
                    'account_id': payment.payment_method_id.inbound_increase_account_id.id,
                    'company_id': self.env.company.id,
                    'treasury_payment_id': payment.id,
                }
                credit_line = {
                    'name': rec_pay_line_name,
                    'amount_currency': 0.0,
                    'currency_id': currency_id,
                    'debit': 0.0,
                    'credit': payment.amount,
                    'date_maturity': payment.payment_date,
                    'partner_id': payment.partner_id.commercial_partner_id.id,
                    'account_id': payment.payment_method_id.outbound_increase_account_id.id,
                    'company_id': self.env.company.id,
                    'treasury_payment_id': payment.id,
                }
            elif payment.payment_type == 'outfunding':
                rec_pay_line_name += _("Salida Caja Menor")
                debit_line = {
                    'name': rec_pay_line_name,
                    'amount_currency': 0.0,
                    'currency_id': currency_id,
                    'debit': payment.amount,
                    'credit': 0.0,
                    'date_maturity': payment.payment_date,
                    'partner_id': payment.partner_id.commercial_partner_id.id,
                    'account_id': payment.payment_method_id.outbound_increase_account_id.id,
                    'company_id': self.env.company.id,
                    'treasury_payment_id': payment.id,
                }
                credit_line = {
                    'name': rec_pay_line_name,
                    'amount_currency': 0.0,
                    'currency_id': currency_id,
                    'debit': 0.0,
                    'credit': payment.amount,
                    'date_maturity': payment.payment_date,
                    'partner_id': payment.partner_id.commercial_partner_id.id,
                    'account_id': payment.payment_method_id.outbound_increase_account_id.id,
                    'company_id': self.env.company.id,
                    'treasury_payment_id': payment.id,
                }
            move_vals = {
                'date': payment.payment_date,
                'ref': payment.name,
                'journal_id': payment.journal_id.id,
                'currency_id': payment.journal_id.currency_id.id or payment.company_id.currency_id.id,
                'partner_id': payment.partner_id.id,
                'company_id': self.env.company.id,
                'treasury_payment_id': payment.id,
                'line_ids': [
                    (0, 0, debit_line),
                    (0, 0, credit_line),
                ],
            }
            all_move_vals.append(move_vals)

        return all_move_vals
    
    def cancel(self):
        self.write({'state': 'cancelled'})

    def unlink(self):
        if any(bool(rec.move_line_ids) for rec in self):
            raise UserError(_("You cannot delete a payment that is already posted."))
        if any(rec.move_name for rec in self):
            raise UserError(_('It is not allowed to delete a payment that already created a journal entry \
            since it would create a gap in the numbering. You should create the journal entry again and cancel it thanks to a regular revert.'))
        return super(account_payment, self).unlink()
    
    def button_journal_entries(self):
        return {
            'name': _('Apuntes Contables'),
            'view_mode': 'tree,form',
            'res_model': 'account.move.line',
            'view_id': False,
            'type': 'ir.actions.act_window',
            'domain': [('treasury_payment_id', 'in', self.ids)],
        }

    def post(self):
        AccountMove = self.env['account.move'].with_context(default_type='entry')
        for rec in self:
            if rec.state != 'draft':
                raise UserError(_("Only a draft payment can be posted."))
                
            if rec.payment_type == 'inbound':
                sequence_code = 'treasury.payment.inbound'
            if rec.payment_type == 'outbound':
                sequence_code = 'treasury.payment.outbound'
            if rec.payment_type == 'infunding':
                sequence_code = 'treasury.payment.infunding'
            if rec.payment_type == 'outfunding':
                sequence_code = 'treasury.payment.outfunding'

            if not rec.name:
                rec.name = self.env['ir.sequence'].next_by_code(sequence_code, sequence_date=rec.payment_date)
                if not rec.name:
                    raise UserError(_("You have to define a sequence for %s in your company.") % (sequence_code,))

            moves = AccountMove.create(rec._prepare_payment_moves())
            moves.filtered(lambda move: move.journal_id.post_at != 'bank_rec').post()
            rec.write({'state': 'posted', 'move_id': moves.id})
            moves.write({'treasury_payment_id': rec.id})

        return True
    
    def action_wizard_payment_conciled_move(self):
        return {
            'name': _('Ver Asiento Conciliación'),
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'view_mode': 'tree,form',
            'view_type': 'tree',
            'domain': [('id', '=', self.treasury_move_id.id)],
            'target': 'current',
            'nodestroy': True,
            'flags': {'initial_mode': 'edit'},
        }

    def action_wizard_payment_consignment_file(self):
        return {
            'name': _('Ver Soporte de Consignación'),
            'type': 'ir.actions.act_url',
            'url': '/web/content/account.payment/%s/contract_template/contract_template.xls?download=true' %(self.id),
        }
    
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4
