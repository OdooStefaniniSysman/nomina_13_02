# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from collections import defaultdict
from datetime import timedelta

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_is_zero
import logging

_logger = logging.getLogger(__name__)


class TreasurySession(models.Model):
    _name = 'treasury.session'
    _order = 'id desc'
    _description = 'Sesiones de Caja Menor'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    TREASURY_SESSION_STATE = [
        ('new_session', 'Nueva Sesión'),
        ('opening_control', 'Control de Apertura'),
        ('opened', 'En progreso'),
        ('closing_control', 'Control de Cierre'),
        ('closed', 'Cerrado y Confirmado'),
    ]
    company_id = fields.Many2one('res.company', related='config_id.company_id', string="Empresa", readonly=True)
    config_id = fields.Many2one(
        'treasury.config', string='Caja Menor',
        help="Caja Menor a la que pertenece la Sesión",
        required=True,
        index=True)
    name = fields.Char(string='Sesión ID', required=True, readonly=True, default='/')
    user_id = fields.Many2one(
        'res.users', string='Responsable',
        required=True,
        index=True,
        readonly=True,
        states={'opening_control': [('readonly', False)]},
        default=lambda self: self.env.uid,
        ondelete='restrict')
    user2_id = fields.Many2one(
        'res.users', string='Responsable',
        required=True,
        compute='_compute_current_admin_user',
        index=True,
        readonly=False,
        states={'opening_control': [('readonly', False)]},
        default=lambda self: self.env.uid,
        ondelete='restrict')
    currency_id = fields.Many2one('res.currency', related='config_id.currency_id', string="Moneda", readonly=False)
    start_at = fields.Datetime(string='Fecha de Apertura', readonly=True)
    stop_at = fields.Datetime(string='Fecha de Cierre', readonly=True, copy=False)
    state = fields.Selection(
        TREASURY_SESSION_STATE, string='Estado',
        required=True, readonly=True,
        index=True, copy=False, default='new_session')
    sequence_number = fields.Integer(string='Contador de Transacciones', help='Un número de secuencia que se incrementa con cada transacción.', default=1)
    cash_control = fields.Boolean(compute='_compute_cash_all', string='Tiene Control de Efectivo', compute_sudo=True)
    cash_journal_id = fields.Many2one('account.journal', compute='_compute_cash_all', string='Diario de Caja', store=True)
    cash_register_id = fields.Many2one('account.bank.statement', compute='_compute_cash_all', string='Caja Registradora', store=True)
    cash_register_balance_end_real = fields.Monetary(
        related='cash_register_id.balance_end_real',
        string="Balance Final",
        help="Total of closing cash control lines.",
        readonly=True)
    cash_register_balance_start = fields.Monetary(
        related='cash_register_id.balance_start',
        string="Balance de Apertura",
        help="Total of opening cash control lines.",
        readonly=True)
    cash_register_total_entry_inbound = fields.Monetary(
        compute='_compute_cash_balance',
        string='Total de Transacciones en Efectivo',
        readonly=True,
        help="Total of all paid sales orders")
    cash_register_total_entry_outbound = fields.Monetary(
        compute='_compute_cash_balance',
        string='Total de Transacciones en Efectivo',
        readonly=True,
        help="Total of all paid sales orders")
    cash_register_total_entry_infunding = fields.Monetary(
        compute='_compute_cash_balance',
        string='Total de Transacciones en Efectivo',
        readonly=True,
        help="Total of all paid sales orders")
    cash_register_total_entry_outfunding = fields.Monetary(
        compute='_compute_cash_balance',
        string='Total de Transacciones en Efectivo',
        readonly=True,
        help="Total of all paid sales orders")
    cash_register_balance_end = fields.Monetary(
        compute='_compute_cash_balance',
        string="Balance de Cierre Teórico",
        help="Sum of opening balance and transactions.",
        readonly=True)
    cash_register_difference = fields.Monetary(
        compute='_compute_cash_balance',
        string='Diferencia',
        help="Diferencia entre el saldo de cierre teórico y el saldo de cierre real.",
        readonly=True)
    cash_register_consigned = fields.Monetary(
        #compute='_compute_cash_balance',
        string='Total Consignado',
        help="Diferencia entre los ingresos de caja y los marcados como consignados.",
        readonly=True)
    bank_register_total_entry_encoding = fields.Monetary(
        compute='_compute_cash_balance',
        string='Total de Transacciones de Banco',
        readonly=True,
        help="Total de Transacciones de Banco o de medios de pago diferentes al Efectivo")
    #move_ids = fields.One2many('sale.order', 'session_id',  string='Asientos de Caja Menor')
    payment_inbound_ids = fields.One2many('treasury.payment', 'session_id',  string='Entradas', domain=[('payment_type', 'in', [('inbound')])])
    payment_outbound_ids = fields.One2many('treasury.payment', 'session_id',  string='Salidas', domain=[('payment_type', 'in', [('outbound')])])
    order_count = fields.Integer(compute='_compute_order_count')
    payment_infunding_ids = fields.One2many('treasury.payment', 'session_id',  string='Aumento de Fondos', domain=[('payment_type', 'in', [('infunding')])])
    payment_outfunding_ids = fields.One2many('treasury.payment', 'session_id',  string='Disminución de Fondos', domain=[('payment_type', 'in', [('outfunding')])])
    move_open_id = fields.Many2one('account.move','Asiento Apertura')
    move_close_id = fields.Many2one('account.move','Asiento Cierre')
    
    statement_ids = fields.One2many('account.bank.statement', 'treasury_session_id', string='Estados de Caja Menor', readonly=True)
    rescue = fields.Boolean(string='Recovery Session',
        help="Auto-generated session for orphan orders, ignored in constraints",
        readonly=True,
        copy=False)
    payment_method_ids = fields.Many2many('treasury.payment.method', related='config_id.payment_method_ids', string='Metodos de Pago')
    total_inbound_payments_amount = fields.Float(compute='_compute_total_payments_amount', string='Total de Ingresos')
    total_outbound_payments_amount = fields.Float(compute='_compute_total_payments_amount', string='Total de Egresos')
    total_infunding_payments_amount = fields.Float(compute='_compute_total_payments_amount', string='Aumento de Fondos')
    total_outfunding_payments_amount = fields.Float(compute='_compute_total_payments_amount', string='Disminución de Fondos')
    is_in_company_currency = fields.Boolean('Está utilizando la moneda de la empresa', compute='_compute_is_in_company_currency')
    session_close_file = fields.Binary(
        string='Adjunto de Cierre de Sesión',
    )

    _sql_constraints = [('uniq_name', 'unique(name)', "El nombre de esta Sesión de Caja Menor debe ser único !")]


    @api.depends('state')
    def _compute_current_admin_user(self):
        if not self.config_id.user2_id.id:
            raise ValidationError(_("Debe definir un Administrador en la configuración de la caja menor"))
        self.user2_id = self.config_id.user2_id.id


    @api.depends('currency_id', 'company_id.currency_id')
    def _compute_is_in_company_currency(self):
        for session in self:
            session.is_in_company_currency = session.currency_id == session.company_id.currency_id

    @api.depends(
        'payment_method_ids',
        'payment_inbound_ids',
        'payment_outbound_ids',
        'payment_infunding_ids',
        'payment_outfunding_ids',
        'cash_register_balance_start',
        'cash_register_id',
        'payment_inbound_ids',
        'payment_outbound_ids')
    def _compute_cash_balance(self):
        for session in self:
            cash_payment_method = session.payment_method_ids.filtered('is_cash_count')[:1]
            if cash_payment_method:
                total_cash_payment = 0
                total_bank_payment = 0
                payment_data = self.env['treasury.payment'].search([('session_id', 'in', self.ids),('state','!=','cancelled'),('state','!=','draft')])
                for payment in payment_data:
                    if payment.journal_id.type == 'cash':
                        total_cash_payment += payment.amount
                    elif payment.journal_id.type == 'bank':
                        total_bank_payment += payment.amount
                session.bank_register_total_entry_encoding = total_bank_payment
                session.cash_register_total_entry_inbound = sum(payment_data.filtered(lambda line: line.payment_type in ('inbound')).mapped('amount'))
                session.cash_register_total_entry_outbound = sum(payment_data.filtered(lambda line: line.payment_type in ('outbound')).mapped('amount'))
                session.cash_register_total_entry_infunding = sum(payment_data.filtered(lambda line: line.payment_type in ('infunding')).mapped('amount'))
                session.cash_register_total_entry_outfunding = sum(payment_data.filtered(lambda line: line.payment_type in ('outfunding')).mapped('amount'))
                session.cash_register_balance_end = session.cash_register_balance_start + session.cash_register_total_entry_inbound + session.cash_register_total_entry_infunding - session.cash_register_total_entry_outbound - session.cash_register_total_entry_outfunding
                session.cash_register_difference = session.cash_register_balance_end_real - (session.cash_register_balance_end - session.cash_register_consigned)
                payment_data = self.env['treasury.payment'].search([
                    ('session_id', 'in', self.ids),
                    ('state','!=','cancel'),
                    ('state','!=','draft'),
                    ('validate_consignation_ok','=',True),
                ])
            else:
                session.cash_register_total_entry_inbound = 0.0
                session.cash_register_total_entry_outbound = 0.0
                session.cash_register_total_entry_infunding = 0.0
                session.cash_register_total_entry_outfunding = 0.0
                session.cash_register_balance_end = 0.0
                session.cash_register_difference = 0.0
                session.cash_register_consigned = 0.0
                session.bank_register_total_entry_encoding = 0.0
    
    def _compute_total_payments_amount(self):
        for session in self:
            session.total_inbound_payments_amount = 0
            session.total_outbound_payments_amount = 0
            payment_inbound_ids = self.env['treasury.payment'].search([('session_id', 'in', self.ids),('state','!=','cancel'),('state','!=','draft')])
            
            session.total_inbound_payments_amount = sum(session.payment_inbound_ids.mapped('amount'))
            session.total_outbound_payments_amount = sum(session.payment_outbound_ids.mapped('amount'))
            session.total_infunding_payments_amount = sum(session.payment_infunding_ids.mapped('amount'))
            session.total_outfunding_payments_amount = sum(session.payment_outfunding_ids.mapped('amount'))
            payment_outbound_ids = self.env['treasury.payment'].search([('session_id', 'in', self.ids),('state','!=','cancel'),('state','!=','draft')])     
            #for payment in payment_data:
            #    session.total_payments_amount += payment.amount
    
    def _compute_total_expenses_amount(self):
        for session in self:
            session.total_expenses_amount = 0
            expense_data = self.env['hr.expense'].search([('session_id', 'in', self.ids),('state','!=','cancel'),('state','!=','draft')])
            for expense in expense_data:
                session.total_expenses_amount += expense.total_amount
    
    def _compute_order_count(self):
        orders_data = self.env['sale.order'].read_group([('session_id', 'in', self.ids),('state','!=','cancel'),('state','!=','draft')], ['session_id'], ['session_id'])
        sessions_data = {order_data['session_id'][0]: order_data['session_id_count'] for order_data in orders_data}
        for session in self:
            session.order_count = sessions_data.get(session.id, 0)

    @api.depends('config_id', 'statement_ids', 'payment_method_ids')
    def _compute_cash_all(self):
        for session in self:
            session.cash_journal_id = session.cash_register_id = session.cash_control = False
            cash_payment_methods = session.payment_method_ids.filtered('is_cash_count')
            for statement in session.statement_ids:
                if statement.journal_id == cash_payment_methods[0].cash_journal_id:
                    session.cash_control = session.config_id.cash_control
                    session.cash_journal_id = statement.journal_id.id
                    session.cash_register_id = statement.id
                    
                    break
    
    @api.constrains('config_id')
    def _check_treasury_config(self):
        if self.search_count([
                ('state', '!=', 'closed'),
                ('config_id', '=', self.config_id.id),
                ('rescue', '=', False)
            ]) > 1:
            raise ValidationError(_("Otra sesión se encuentra abierta para esta misma caja menor."))

    @api.constrains('start_at')
    def _check_start_date(self):
        for record in self:
            company = record.config_id.journal_id.company_id
            start_date = record.start_at.date()
            if (company.period_lock_date and start_date <= company.period_lock_date) or (company.fiscalyear_lock_date and start_date <= company.fiscalyear_lock_date):
                raise ValidationError(_("You cannot create a session before the accounting lock date."))

    @api.model
    def create(self, values):
        config_id = values.get('config_id') or self.env.context.get('default_config_id')
        if not config_id:
            raise UserError(_("Debe asignar una caja menor a su sesión."))

        treasury_config = self.env['treasury.config'].browse(config_id)
        ctx = dict(self.env.context, company_id=treasury_config.company_id.id)
        treasury_name = self.env['ir.sequence'].search([('id','=',treasury_config.sequence_id.id)]).next_by_id()
        if values.get('name'):
            treasury_name += ' ' + values['name']
        cash_payment_methods = treasury_config.payment_method_ids.filtered(lambda pm: pm.is_cash_count)
        statement_ids = self.env['account.bank.statement']
        if self.user_has_groups('point_of_sale.group_treasury_user'):
            statement_ids = statement_ids.sudo()
        for cash_journal in cash_payment_methods.mapped('cash_journal_id'):
            ctx['journal_id'] = cash_journal.id if treasury_config.cash_control and cash_journal.type == 'cash' else False
            st_values = {
                'journal_id': cash_journal.id,
                'user_id': self.env.user.id,
                'name': treasury_name,
                'balance_start': self.env["account.bank.statement"]._get_opening_balance(cash_journal.id) if cash_journal.type == 'cash' else 0
            }
            statement_ids |= statement_ids.with_context(ctx).create(st_values)
        values.update({
            'name': treasury_name,
            'statement_ids': [(6, 0, statement_ids.ids)],
            'config_id': config_id,
        })
        if self.user_has_groups('point_of_sale.group_treasury_user'):
            res = super(TreasurySession, self.with_context(ctx).sudo()).create(values)
        else:
            res = super(TreasurySession, self.with_context(ctx)).create(values)
        if not treasury_config.cash_control:
            res.action_treasury_session_open()
        return res

    def unlink(self):
        for session in self.filtered(lambda s: s.statement_ids):
            session.statement_ids.unlink()
        return super(TreasurySession, self).unlink()

    def login(self):
        self.ensure_one()
        login_number = self.login_number + 1
        self.write({
            'login_number': login_number,
        })
        return login_number
    
    def _prepare_payment_moves_open(self):
        all_move_vals = []
        for session in self:
            company_currency = session.company_id.currency_id
            
            if self.env.company.currency_id == session.company_id.currency_id:
                counterpart_amount = write_off_amount = 0.0
                balance = counterpart_amount
                write_off_balance = write_off_amount
                currency_id = False
            else:
                raise UserError(_("El módulo de cajas menores no soporte transacciones en una moneda diferente a la moneda de la compañía actual."))
                
            if session.cash_register_balance_start <= 0:
                raise UserError(_("El balance inicial no puede ser negativo."))
            
           
            
            rec_pay_line_name = ''
            rec_pay_line_name += _("Apertura de Caja Menor")
            debit_line = {
                'name': rec_pay_line_name,
                'amount_currency': 0.0,
                'currency_id': currency_id,
                'debit': session.cash_register_balance_start,
                'credit': 0,
                'date_maturity': session.start_at,
                'partner_id': session.company_id.partner_id.commercial_partner_id.id,
                'account_id': session.payment_method_ids.filtered(lambda line: line.is_cash_count is True).mapped('inbound_open_account_id').id,
                'company_id': self.env.company.id,
                'treasury_session_id': session.id,
            }
            credit_line = {
                'name': rec_pay_line_name,
                'amount_currency': 0.0,
                'currency_id': currency_id,
                'debit': 0.0,
                'credit': session.cash_register_balance_start,
                'date_maturity': session.start_at,
                'partner_id': session.company_id.partner_id.commercial_partner_id.id,
                'account_id': session.payment_method_ids.filtered(lambda line: line.is_cash_count is True).mapped('outbound_open_account_id').id,
                'company_id': self.env.company.id,
                'treasury_session_id': session.id,
            }
            move_vals = {
                'date': session.start_at,
                'ref': session.name,
                'journal_id': session.payment_method_ids.filtered(lambda line: line.is_cash_count is True).mapped('cash_journal_id').id,
                'currency_id': session.company_id.currency_id.id or self.env.company_id,
                'partner_id': session.company_id.partner_id.commercial_partner_id.id,
                'company_id': self.env.company.id,
                'treasury_session_id': session.id,
                'line_ids': [
                    (0, 0, debit_line),
                    (0, 0, credit_line),
                ],
            }
            all_move_vals.append(move_vals)
        return all_move_vals

    def action_treasury_session_open(self):
        for session in self.filtered(lambda session: session.state in ('new_session', 'opening_control')):
            values = {}
            if not session.start_at:
                values['start_at'] = fields.Datetime.now()
            values['state'] = 'opened'
            session.write(values)
            session.statement_ids.button_open()
            AccountMove = self.env['account.move'].with_context(default_type='entry')
            for rec in self:                
                if not rec.name:
                    rec.name = self.env['ir.sequence'].next_by_code('sequence_treasury_open_session', sequence_date=rec.stop_at)
                    if not rec.name:
                        raise UserError(_("You have to define a sequence for %s in your company.") % (sequence_code,))
                moves = AccountMove.create(rec._prepare_payment_moves_open())
                moves.filtered(lambda move: move.journal_id.post_at != 'bank_rec').post()
                rec.write({'move_open_id': moves.id})
                moves.write({'treasury_session_id': rec.id})
        return True

    def action_treasury_session_closing_control(self):
        self._check_treasury_session_balance()
        for session in self:
            session.write({'state': 'closing_control', 'stop_at': fields.Datetime.now()})
            if not session.config_id.cash_control:
                session.action_treasury_session_close()

    def _check_treasury_session_balance(self):
        for session in self:
            for statement in session.statement_ids:
                if (statement != session.cash_register_id) and (statement.balance_end != statement.balance_end_real):
                    statement.write({'balance_end_real': statement.balance_end})

    def action_treasury_session_validate(self):
        self._check_treasury_session_balance()
        return self.action_treasury_session_close()

    def action_treasury_session_close(self):
        if not self.cash_register_id:
            return self._validate_session()

        if self.cash_control and abs(self.cash_register_difference) > self.config_id.amount_authorized_diff:
            # Only pos manager can close statements with cash_register_difference greater than amount_authorized_diff.
            if not self.user_has_groups("point_of_sale.group_treasury_manager"):
                raise UserError(_(
                    "Su saldo final es demasiado diferente del cierre de caja teórico (%.2f), "
                    "el máximo permitido es: %.2f. Puede contactar a su director para forzarlo."
                ) % (self.cash_register_difference, self.config_id.amount_authorized_diff))
            else:
                return self._warning_balance_closing()
        else:
            return self._validate_session()
        
    def _prepare_payment_moves_close(self):
        all_move_vals = []
        for session in self:
            company_currency = session.company_id.currency_id
            
            if self.env.company.currency_id == session.company_id.currency_id:
                counterpart_amount = write_off_amount = 0.0
                balance = counterpart_amount
                write_off_balance = write_off_amount
                currency_id = False
            else:
                raise UserError(_("El módulo de cajas menores no soporte transacciones en una moneda diferente a la moneda de la compañía actual."))
                
            if session.cash_register_balance_end_real <= 0:
                raise UserError(_("El balance final no puede ser negativo."))

            rec_pay_line_name = ''
            rec_pay_line_name += _("Cierre de Caja Menor")
            debit_line = {
                'name': rec_pay_line_name,
                'amount_currency': 0.0,
                'currency_id': currency_id,
                'debit': session.cash_register_balance_end_real,
                'credit': 0,
                'date_maturity': session.stop_at,
                'partner_id': session.company_id.partner_id.commercial_partner_id.id,
                'account_id': session.payment_method_ids.filtered(lambda line: line.is_cash_count is True).mapped('outbound_close_account_id').id,
                'company_id': self.env.company.id,
                'treasury_payment_id': session.id,
            }
            credit_line = {
                'name': rec_pay_line_name,
                'amount_currency': 0.0,
                'currency_id': currency_id,
                'debit': 0.0,
                'credit': session.cash_register_balance_end_real,
                'date_maturity': session.stop_at,
                'partner_id': session.company_id.partner_id.commercial_partner_id.id,
                'account_id': session.payment_method_ids.filtered(lambda line: line.is_cash_count is True).mapped('inbound_close_account_id').id,
                'company_id': self.env.company.id,
                'treasury_session_id': session.id,
            }
            move_vals = {
                'date': session.stop_at,
                'ref': session.name,
                'journal_id': session.payment_method_ids.filtered(lambda line: line.is_cash_count is True).mapped('cash_journal_id').id,
                'currency_id': session.company_id.currency_id.id or self.env.company_id,
                'partner_id': session.company_id.partner_id.commercial_partner_id.id,
                'company_id': self.env.company.id,
                'treasury_session_id': session.id,
                'line_ids': [
                    (0, 0, debit_line),
                    (0, 0, credit_line),
                ],
            }
            all_move_vals.append(move_vals)

        return all_move_vals

    def _validate_session(self):
        self.ensure_one()
        self._check_if_no_draft_payments()
        self._check_if_no_file_close()
        self.write({'state': 'closed'})
        AccountMove = self.env['account.move'].with_context(default_type='entry')
        for rec in self:                
            if not rec.name:
                rec.name = self.env['ir.sequence'].next_by_code('sequence_treasury_close_session', sequence_date=rec.stop_at)
                if not rec.name:
                    raise UserError(_("You have to define a sequence for %s in your company.") % (sequence_code,))

            moves = AccountMove.create(rec._prepare_payment_moves_close())
            moves.filtered(lambda move: move.journal_id.post_at != 'bank_rec').post()
            rec.write({'move_close_id': moves.id})
            moves.write({'treasury_payment_id': rec.id})
            
        return {
            'type': 'ir.actions.client',
            'name': 'Menú Cajas Menores',
            'tag': 'reload',
            'params': {'menu_id': self.env.ref('account_petty_cash.menu_treasury_root').id},
        }
   
    def _update_amounts(self, old_amounts, amounts_to_add, date, round=True):
        new_amounts = {}
        for k, amount in old_amounts.items():
            if k == 'amount_converted':
                amount_converted = old_amounts['amount_converted']
                amount_to_convert = amounts_to_add['amount']
                new_amounts['amount_converted'] = amount_converted if self.is_in_company_currency else (
                    amount_converted + self._amount_converter(amount_to_convert, date, round))
            else:
                new_amounts[k] = old_amounts[k] + amounts_to_add[k]
        return new_amounts

    def _round_amounts(self, amounts):
        new_amounts = {}
        for key, amount in amounts.items():
            if key == 'amount_converted':
                # round the amount_converted using the company currency.
                new_amounts[key] = self.company_id.currency_id.round(amount)
            else:
                new_amounts[key] = self.currency_id.round(amount)
        return new_amounts

    def _amount_converter(self, amount, date, round):
        # self should be single record as this method is only called in the subfunctions of self._validate_session
        return self.currency_id._convert(amount, self.company_id.currency_id, self.company_id, date, round=round)

    def action_show_payments_inbound_list(self):
        if self.state != 'opened':
            return {
                'name': _('Entradas'),
                'type': 'ir.actions.act_window',
                'res_model': 'treasury.payment',
                'view_mode': 'tree',
                'views': [
                    (self.env.ref('account_petty_cash.view_treasury_payment_tree').id, 'tree'),
                ],
                'domain': [('session_id', '=', self.id),('payment_type','=','inbound')],
                'context': {
                    'search_default_group_by_journal_id': 1,
                    'default_payment_type': 'inbound',
                    'default_session_id': self.id,
                }
            }
        return {
            'name': _('Entradas'),
            'type': 'ir.actions.act_window',
            'res_model': 'treasury.payment',
            'view_mode': 'tree,form',
            'views': [
                (self.env.ref('account_petty_cash.view_treasury_payment_tree').id, 'tree'),
                (self.env.ref('account_petty_cash.view_treasury_payment_form').id, 'form'),
            ],
            'domain': [('session_id', '=', self.id),('payment_type','=','inbound')],
            'context': {
                'search_default_group_by_journal_id': 1,
                'default_payment_type': 'inbound',
                'default_session_id': self.id,
            }
        }
    
    def action_show_payments_outbound_list(self):
        if self.state != 'opened':
            raise UserError(_("No puede registrar transacciones en una Caja Menor que no este en estado Progreso"))
        return {
            'name': _('Salidas'),
            'type': 'ir.actions.act_window',
            'res_model': 'treasury.payment',
            'view_mode': 'tree,form',
            'views': [
                (self.env.ref('account_petty_cash.view_treasury_payment_tree').id, 'tree'),
                (self.env.ref('account_petty_cash.view_treasury_payment_form').id, 'form'),
            ],
            'domain': [('session_id', '=', self.id),('payment_type', '=', 'outbound')],
            'context': {
                'search_default_group_by_journal_id': 1,
                'default_payment_type': 'outbound',
                'default_session_id': self.id,
            }
        }
    
    def action_show_payments_infunding_list(self):
        if self.state != 'opened':
            return {
                'name': _('Aumento de Fondos'),
                'type': 'ir.actions.act_window',
                'res_model': 'treasury.payment',
                'view_mode': 'tree',
                'views': [
                    (self.env.ref('account_petty_cash.view_treasury_payment_tree').id, 'tree'),
                ],
                'domain': [('session_id', '=', self.id),('payment_type', '=', 'infunding')],
                'context': {
                    'search_default_group_by_journal_id': 1,
                    'default_payment_type': 'infunding',
                    'default_session_id': self.id,
                }
            }
        return {
            'name': _('Aumento de Fondos'),
            'type': 'ir.actions.act_window',
            'res_model': 'treasury.payment',
            'view_mode': 'tree,form',
            'views': [
                (self.env.ref('account_petty_cash.view_treasury_payment_tree').id, 'tree'),
                (self.env.ref('account_petty_cash.view_treasury_payment_form').id, 'form'),
            ],
            'domain': [('session_id', '=', self.id),('payment_type', '=', 'infunding')],
            'context': {
                'search_default_group_by_journal_id': 1,
                'default_payment_type': 'infunding',
                'default_session_id': self.id,
            }
        }
    
    def action_show_payments_outfunding_list(self):
        if self.state != 'opened':
            return {
                'name': _('Disminución de Fondos'),
                'type': 'ir.actions.act_window',
                'res_model': 'treasury.payment',
                'view_mode': 'form',
                'views': [
                    (self.env.ref('account_petty_cash.view_treasury_payment_tree').id, 'tree'),
                ],
                'domain': [('session_id', '=', self.id),('payment_type', '=', 'outfunding')],
                'context': {
                    'search_default_group_by_journal_id': 1,
                    'default_payment_type': 'outfunding',
                    'default_session_id': self.id,
                }
            }
        return {
            'name': _('Disminución de Fondos'),
            'type': 'ir.actions.act_window',
            'res_model': 'treasury.payment',
            'view_mode': 'tree,form',
            'views': [
                (self.env.ref('account_petty_cash.view_treasury_payment_tree').id, 'tree'),
                (self.env.ref('account_petty_cash.view_treasury_payment_form').id, 'form'),
            ],
            'domain': [('session_id', '=', self.id),('payment_type', '=', 'outfunding')],
            'context': {
                'search_default_group_by_journal_id': 1,
                'default_payment_type': 'outfunding',
                'default_session_id': self.id,
            }
        }

    def open_cashbox_treasury(self):
        self.ensure_one()
        action = self.cash_register_id.open_cashbox_id()
        action['view_id'] = self.env.ref('account_petty_cash.view_account_bnk_stmt_cashbox_footer').id
        action['context']['treasury_session_id'] = self.id
        action['context']['default_treasury_id'] = self.config_id.id
        return action

    def action_view_order(self):
        return {
            'name': _('Ordenes de Venta'),
            'res_model': 'sale.order',
            'view_mode': 'tree,form',
            'views': [
                (self.env.ref('sale.view_order_tree').id, 'tree'),
                (self.env.ref('sale.view_order_form').id, 'form'),
                ],
            'type': 'ir.actions.act_window',
            'domain': [('session_id', 'in', self.ids)],
        }

    def _warning_balance_closing(self):
        self.ensure_one()

        context = dict(self._context)
        context['session_id'] = self.id

        return {
            'name': _('Balance control'),
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'closing.balance.confirm.wizard',
            'views': [(False, 'form')],
            'type': 'ir.actions.act_window',
            'context': context,
            'target': 'new'
        }
    
    
    def _check_if_no_draft_payments(self):
        #draft_orders = self.order_ids.filtered(lambda order: order.state == 'draft')
        #draft_payments = self.payment_ids.filtered(lambda payment: payment.state == 'draft')
        #if draft_payments:
        #    raise UserError(_(
        #            'Existen ingresos en estado borrador incluidos en esta sesión. '
        #            'Confirme o anule los siguientes ingresos para poder validar la sesión:\n%s'
        #        ) % ', '.join(draft_payments.mapped('name'))
        #   )
        return True
    
	
    def _check_if_no_file_close(self):
        if not self.session_close_file:
            raise UserError(_('¡Debe adjuntar el archivo requerido de cierre antes de finalizar sesión! ...'))
        return True

class ProcurementGroup(models.Model):
    _inherit = 'procurement.group'

    @api.model
    def _run_scheduler_tasks(self, use_new_cursor=False, company_id=False):
        super(ProcurementGroup, self)._run_scheduler_tasks(use_new_cursor=use_new_cursor, company_id=company_id)
        self.env['treasury.session']._alert_old_session()
        if use_new_cursor:
            self.env.cr.commit()

class ClosingBalanceConfirm(models.TransientModel):
    _name = 'closing.balance.confirm.wizard'
    _description = '''This wizard is used to display a warning message if the manager wants to 
                        close a session with a too high difference between real and expected closing balance'''

    def confirm_closing_balance(self):
        current_session =  self.env['treasury.session'].browse(self._context['session_id'])
        return current_session._validate_session()
