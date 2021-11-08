# -*- coding: utf-8 -*-

from datetime import datetime
from uuid import uuid4

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError


class AccountBankStmtCashWizard(models.Model):
    _inherit = 'account.bank.statement.cashbox'

    @api.depends('treasury_config_ids')
    @api.depends_context('current_currency_id')
    def _compute_currency(self):
        super(AccountBankStmtCashWizard, self)._compute_currency()
        for cashbox in self:
            if cashbox.treasury_config_ids:
                cashbox.currency_id = cashbox.treasury_config_ids[0].currency_id.id
            elif self.env.context.get('current_currency_id'):
                cashbox.currency_id = self.env.context.get('current_currency_id')

    treasury_config_ids = fields.One2many('treasury.config', 'default_cashbox_id')
    is_a_template = fields.Boolean(default=False)

    @api.model
    def default_get(self, fields):
        vals = super(AccountBankStmtCashWizard, self).default_get(fields)
        if "is_a_template" in fields and self.env.context.get('default_is_a_template'):
            vals['is_a_template'] = True
        config_id = self.env.context.get('default_treasury_id')
        if config_id:
            config = self.env['treasury.config'].browse(config_id)
            if config.last_session_closing_cashbox.cashbox_lines_ids:
                lines = config.last_session_closing_cashbox.cashbox_lines_ids
            else:
                lines = config.default_cashbox_id.cashbox_lines_ids
            if self.env.context.get('balance', False) == 'start':
                vals['cashbox_lines_ids'] = [[0, 0, {'coin_value': line.coin_value, 'number': line.number, 'subtotal': line.subtotal}] for line in lines]
            else:
                vals['cashbox_lines_ids'] = [[0, 0, {'coin_value': line.coin_value, 'number': 0, 'subtotal': 0.0}] for line in lines]
        return vals

    def _validate_cashbox(self):
        super(AccountBankStmtCashWizard, self)._validate_cashbox()
        session_id = self.env.context.get('treasury_session_id')
        if session_id:
            current_session = self.env['treasury.session'].browse(session_id)
            if current_session.state == 'new_session':
                current_session.write({'state': 'opening_control'})

    def set_default_cashbox(self):
        self.ensure_one()
        current_session = self.env['treasury.session'].browse(self.env.context['treasury_session_id'])
        lines = current_session.config_id.default_cashbox_id.cashbox_lines_ids
        context = dict(self._context)
        self.cashbox_lines_ids.unlink()
        self.cashbox_lines_ids = [[0, 0, {'coin_value': line.coin_value, 'number': line.number, 'subtotal': line.subtotal}] for line in lines]

        return {
            'name': _('Control de Efectivo'),
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'account.bank.statement.cashbox',
            'view_id': self.env.ref('account_petty_cash.view_account_bnk_stmt_cashbox_footer').id,
            'type': 'ir.actions.act_window',
            'context': context,
            'target': 'new',
            'res_id': self.id,
        }


class TreasuryConfig(models.Model):
    _name = 'treasury.config'
    _description = 'Configuración de una Caja Menor de Tesorería'

    def _get_group_treasury_manager(self):
        return self.env.ref('account_petty_cash.group_treasury_manager')

    def _get_group_treasury_user(self):
        return self.env.ref('account_petty_cash.group_treasury_user')

    def _default_sale_journal(self):
        return self.env['account.journal'].search([('type', '=', 'sale'), ('company_id', '=', self.env.company.id), ('code', '=', 'TREASURY')], limit=1)

    def _default_payment_methods(self):
        return self.env['treasury.payment.method'].search([('split_transactions', '=', False), ('company_id', '=', self.env.company.id)])


    name = fields.Char(string='Caja Menor', index=True, required=True, help="Un identificador interno para la caja menor de tesorería.")
    currency_id = fields.Many2one('res.currency', compute='_compute_currency', string="Moneda")
    cash_control = fields.Boolean(string='Control de Efectivo', help="Verifique el monto de la caja menor al abrir y cerrar.")
    active = fields.Boolean(default=True)
    uuid = fields.Char(readonly=True, default=lambda self: str(uuid4()),
        help='Identificador único global para esta configuración de tesorería.')
    sequence_id = fields.Many2one('ir.sequence', string='Secuencia de la Caja', readonly=True,
        help="Secuencia automatica, que se puede modificar", copy=False, ondelete='restrict')
    sequence_line_id = fields.Many2one('ir.sequence', string='Secuencia de Transacciones', readonly=True,
        help="Secuencia automatica, que se puede modificar", copy=False)
    session_ids = fields.One2many('treasury.session', 'config_id', string='Sesiones')
    current_session_id = fields.Many2one('treasury.session', compute='_compute_current_session', string="Sesión Actual")
    current_session_state = fields.Char(compute='_compute_current_session')
    last_session_closing_cash = fields.Float(compute='_compute_last_session')
    last_session_closing_date = fields.Date(compute='_compute_last_session')
    last_session_closing_cashbox = fields.Many2one('account.bank.statement.cashbox', compute='_compute_last_session')
    treasury_session_username = fields.Char(compute='_compute_current_session_user')
    treasury_session_state = fields.Char(compute='_compute_current_session_user')
    treasury_session_duration = fields.Char(compute='_compute_current_session_user')
    journal_id = fields.Many2one(
        'account.journal', string='Diario de la Caja Menor',
        domain=[('type', '=', 'sale')],
        help="Diario de contabilidad utilizado para registrar las transacciones de la caja menor",
        default=_default_sale_journal)
    amount_authorized_diff = fields.Float('Monto de la Diferencia autorizada',
        help="Este campo representa la diferencia máxima permitida entre el saldo final y el efectivo teórico cuando "
             "se cierra una sesión, para administradores que no son de Tesorería. Si se alcanza este máximo, el usuario tendrá un mensaje de error en "
             "el cierre de su sesión diciendo que necesita contactar a su Administrador.")
    iface_precompute_cash = fields.Boolean(string='Pago previo en efectivo',
        help='La entrada de pago se comportará de manera similar a la entrada de pago bancario, y se rellenará previamente con el importe exacto adeudado.')
    company_id = fields.Many2one('res.company', string='Empresa', required=True, default=lambda self: self.env.company)
    default_cashbox_id = fields.Many2one('account.bank.statement.cashbox', string='Balance por Defecto')
    payment_method_ids = fields.Many2many('treasury.payment.method', string='Métodos de Pago', default=lambda self: self._default_payment_methods())
    current_user_id = fields.Many2one('res.users', string='Responsable de la Sesión Actual', compute='_compute_current_session_user')
    user2_id = fields.Many2one('res.users', string='Administrador de la Caja Menor',required=True)
    account_analytic_tag_id = fields.Many2one('account.analytic.tag',string='Etiqueta Analítica para Asientos',required=False)
    account_analytic_id = fields.Many2one('account.analytic.account',string='Cuenta Analítica para Asientos',required=False)

    @api.depends('company_id')
    def _compute_company_has_template(self):
        for config in self:
            if config.company_id.chart_template_id:
                config.company_has_template = True
            else:
                config.company_has_template = False

    @api.depends('journal_id.currency_id', 'journal_id.company_id.currency_id', 'company_id', 'company_id.currency_id')
    def _compute_currency(self):
        for treasury_config in self:
            if treasury_config.journal_id:
                treasury_config.currency_id = treasury_config.journal_id.currency_id.id or treasury_config.journal_id.company_id.currency_id.id
            else:
                treasury_config.currency_id = treasury_config.company_id.currency_id.id

    @api.depends('session_ids', 'session_ids.state')
    def _compute_current_session(self):
        for treasury_config in self:
            session = treasury_config.session_ids.filtered(lambda s: s.user_id.id == self.env.uid and \
                    not s.state == 'closed' and not s.rescue)
            treasury_config.current_session_id = session and session[0].id or False
            treasury_config.current_session_state = session and session[0].state or False

    @api.depends('session_ids')
    def _compute_last_session(self):
        TreasurySession = self.env['treasury.session']
        for treasury_config in self:
            session = TreasurySession.search_read(
                [('config_id', '=', treasury_config.id), ('state', '=', 'closed')],
                ['cash_register_balance_end_real', 'stop_at', 'cash_register_id'],
                order="stop_at desc", limit=1)
            if session:
                treasury_config.last_session_closing_date = session[0]['stop_at'].date()
                if session[0]['cash_register_id']:
                    treasury_config.last_session_closing_cash = session[0]['cash_register_balance_end_real']
                    treasury_config.last_session_closing_cashbox = self.env['account.bank.statement'].browse(session[0]['cash_register_id'][0]).cashbox_end_id
                else:
                    treasury_config.last_session_closing_cash = 0
                    treasury_config.last_session_closing_cashbox = False
            else:
                treasury_config.last_session_closing_cash = 0
                treasury_config.last_session_closing_date = False
                treasury_config.last_session_closing_cashbox = False

    @api.depends('session_ids')
    def _compute_current_session_user(self):
        for treasury_config in self:
            session = treasury_config.session_ids.filtered(
                lambda s: s.state in ['new_session', 'opening_control', 'opened', 'closing_control'] and not s.rescue)
            if session:
                treasury_config.treasury_session_username = session[0].user_id.sudo().name
                treasury_config.treasury_session_state = session[0].state
                treasury_config.treasury_session_duration = (
                    datetime.now() - session[0].start_at
                ).days if session[0].start_at else 0
                treasury_config.current_user_id = session[0].user_id
            else:
                treasury_config.treasury_session_username = False
                treasury_config.treasury_session_state = False
                treasury_config.treasury_session_duration = 0
                treasury_config.current_user_id = False

    @api.constrains('journal_id', 'invoice_journal_id', 'payment_method_ids')
    def _check_currencies(self):
        if any(
            self.payment_method_ids\
                .filtered(lambda pm: pm.is_cash_count)\
                .mapped(lambda pm: self.currency_id not in (self.company_id.currency_id | pm.cash_journal_id.currency_id))
        ):
            raise ValidationError(_("Todos los métodos de pago deben estar en la misma moneda que el Diario asociado o la moneda de la compañía."))

    @api.constrains('cash_control')
    def _check_session_state(self):
        open_session = self.env['treasury.session'].search([('config_id', '=', self.id), ('state', '!=', 'closed')])
        if open_session:
            raise ValidationError(_("No puede cambiar el estado del control de efectivo mientras una sesión ya está abierta."))

    def name_get(self):
        result = []
        for config in self:
            last_session = self.env['treasury.session'].search([('config_id', '=', config.id)], limit=1)
            if (not last_session) or (last_session.state == 'closed'):
                result.append((config.id, config.name + ' (' + _('not used') + ')'))
                continue
            result.append((config.id, config.name + ' (' + last_session.user_id.name + ')'))
        return result

    @api.model
    def create(self, values):
        IrSequence = self.env['ir.sequence'].sudo()
        val = {
            'name': _('Sesión de Caja Menor %s') % values['name'],
            'padding': 4,
            'prefix': "%s/" % values['name'],
            'code': "treasury.session",
            'company_id': values.get('company_id', False),
        }
        values['sequence_id'] = IrSequence.create(val).id
        values['sequence_line_id'] = IrSequence.create(val).id
        treasury_config = super(TreasuryConfig, self).create(values)
        treasury_config.sudo()._check_groups_implied()
        return treasury_config

    def write(self, vals):
        opened_session = self.mapped('session_ids').filtered(lambda s: s.state != 'closed')
        #if opened_session:
        #    raise UserError(_('No se puede modificar esta configuración de la caja menor porque hay una sesión de tesorería abierta basada en ella.'))
        result = super(TreasuryConfig, self).write(vals)
        self.sudo()._check_groups_implied()
        return result

    def unlink(self):
        sequences_to_delete = self.sequence_id | self.sequence_line_id
        res = super(TreasuryConfig, self).unlink()
        sequences_to_delete.unlink()
        return res

    def _check_groups_implied(self):
        for treasury_config in self:
            for field_name in [f for f in treasury_config.fields_get_keys() if f.startswith('group_')]:
                field = treasury_config._fields[field_name]
                if field.type in ('boolean', 'selection') and hasattr(field, 'implied_group'):
                    field_group_xmlids = getattr(field, 'group', 'base.group_user').split(',')
                    field_groups = self.env['res.groups'].concat(*(self.env.ref(it) for it in field_group_xmlids))
                    field_groups.write({'implied_ids': [(4, self.env.ref(field.implied_group).id)]})

    def execute(self):
        return {
             'type': 'ir.actions.client',
             'tag': 'reload',
             'params': {'wait': True}
         }

    def open_session_cb(self):
        self.ensure_one()
        if not self.current_session_id:
            self.env['treasury.session'].create({
                'user_id': self.env.uid,
                'config_id': self.id
            })
            if self.current_session_id.state == 'opened':
                return self._open_session(self.current_session_id.id)
        return self._open_session(self.current_session_id.id)

    def open_existing_session_cb(self):
        self.ensure_one()
        return self._open_session(self.current_session_id.id)

    def _open_session(self, session_id):
        return {
            'name': _('Sesión Caja Menor'),
            'view_mode': 'form,tree',
            'res_model': 'treasury.session',
            'res_id': session_id,
            'view_id': False,
            'type': 'ir.actions.act_window',
        }

    @api.model
    def post_install_treasury_localisation(self):
        self.assign_payment_journals()
        self.generate_treasury_journal()

    @api.model
    def assign_payment_journals(self, companies=False):
        self = self.sudo()
        if not companies:
            companies = self.env['res.company'].search([])
        for company in companies:
            if company.chart_template_id:
                cash_journal = self.env['account.journal'].search([('company_id', '=', company.id), ('type', '=', 'cash')], limit=1)
                treasury_receivable_account = company.account_default_treasury_receivable_account_id
                payment_methods = self.env['treasury.payment.method']
                if cash_journal:
                    payment_methods |= payment_methods.create({
                        'name': _('Cash'),
                        'receivable_account_id': treasury_receivable_account.id,
                        'is_cash_count': True,
                        'cash_journal_id': cash_journal.id,
                        'company_id': company.id,
                    })
                payment_methods |= payment_methods.create({
                    'name': _('Bank'),
                    'receivable_account_id': treasury_receivable_account.id,
                    'is_cash_count': False,
                    'company_id': company.id,
                })
                existing_treasury_config = self.env['treasury.config'].search([('company_id', '=', company.id), ('payment_method_ids', '=', False)])
                existing_treasury_config.write({'payment_method_ids': [(6, 0, payment_methods.ids)]})

    @api.model
    def generate_treasury_journal(self, companies=False):
        self = self.sudo()
        if not companies:
            companies = self.env['res.company'].search([])
        for company in companies:
            treasury_journal = self.env['account.journal'].search([('company_id', '=', company.id), ('code', '=', 'TREASURY')])
            if company.chart_template_id and not treasury_journal:
                treasury_journal = self.env['account.journal'].create({
                    'type': 'sale',
                    'name': 'Tesorería',
                    'code': 'CAJA MENOR',
                    'company_id': company.id,
                    'sequence': 20
                })
                existing_treasury_config = self.env['treasury.config'].search([('company_id', '=', company.id), ('journal_id', '=', False)])
                existing_treasury_config.write({'journal_id': treasury_journal.id})
                
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
