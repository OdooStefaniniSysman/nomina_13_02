# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class TreasuryPaymentMethod(models.Model):
    _name = "treasury.payment.method"
    _description = "Treasury of purchase or sale payment methods for petty cash"
    _order = "id asc"

    def _get_payment_terminal_selection(self):
        return []

    name = fields.Char(string="Metodo de Pago", required=True)
    inbound_open_account_id = fields.Many2one('account.account',
        string='Cuenta de Entrada',
        required=True,
        domain=[('deprecated', '=', False)],
        #default=lambda self: self.env.company.account_default_pos_receivable_account_id,
        ondelete='restrict',
        help='Cuenta para el registro de las entradas durante la apertura de caja')
    
    outbound_open_account_id = fields.Many2one('account.account',
        string='Cuenta de Salida',
        required=True,
        domain=[('deprecated', '=', False)],
        #default=lambda self: self.env.company.account_default_pos_receivable_account_id,
        ondelete='restrict',
        help='Cuenta para el registro de las Salidas durante la apertura de caja.')
    
    inbound_close_account_id = fields.Many2one('account.account',
        string='Cuenta de Entrada',
        required=True,
        domain=[('deprecated', '=', False)],
        #default=lambda self: self.env.company.account_default_pos_receivable_account_id,
        ondelete='restrict',
        help='Cuenta para el registro de las entradas.')
    
    outbound_close_account_id = fields.Many2one('account.account',
        string='Cuenta de Salida',
        required=True,
        domain=[('deprecated', '=', False)],
        #default=lambda self: self.env.company.account_default_pos_receivable_account_id,
        ondelete='restrict',
        help='Cuenta para el registro de las entradas.')
    
    inbound_increase_account_id = fields.Many2one('account.account',
        string='Cuenta de Entrada',
        required=True,
        domain=[('deprecated', '=', False)],
        #default=lambda self: self.env.company.account_default_pos_receivable_account_id,
        ondelete='restrict',
        help='Cuenta para el registro de las entradas.')
    
    outbound_increase_account_id = fields.Many2one('account.account',
        string='Cuenta de Salida',
        required=True,
        domain=[('deprecated', '=', False)],
        #default=lambda self: self.env.company.account_default_pos_receivable_account_id,
        ondelete='restrict',
        help='Cuenta para el registro de las entradas.')
    
    inbound_decrease_account_id = fields.Many2one('account.account',
        string='Cuenta de Entrada',
        required=True,
        domain=[('deprecated', '=', False)],
        #default=lambda self: self.env.company.account_default_pos_receivable_account_id,
        ondelete='restrict',
        help='Cuenta para el registro de las entradas.')
    
    outbound_decrease_account_id = fields.Many2one('account.account',
        string='Cuenta de Salida',
        required=True,
        domain=[('deprecated', '=', False)],
        #default=lambda self: self.env.company.account_default_pos_receivable_account_id,
        ondelete='restrict',
        help='Cuenta para el registro de las entradas.')
    
    is_cash_count = fields.Boolean(string='Efectivo')
    cash_journal_id = fields.Many2one('account.journal',
        string='Diario de Efectivo',
        domain=[('type', '=', 'cash'),('petty_cash_ok', '=', True)],
        ondelete='restrict',
        help='La forma de pago es de tipo efectivo. Se generará automáticamente un estado de caja.')
    split_transactions = fields.Boolean(
        string='Transacciones divididas',
        default=False,
        help='Si está marcado, cada transacción generará una línea de diario separada. Es un proceso más lento')
    open_session_ids = fields.Many2many('treasury.session', 
                                        string='Sesiones de Caja Menor', 
                                        compute='_compute_open_session_ids', 
                                        help='Sesiones abiertas de Caja Menor que utilizan este método de pago.')
    config_ids = fields.Many2many('treasury.config', string='Cajas Menores')
    company_id = fields.Many2one('res.company', string='Empresa', default=lambda self: self.env.company)
    use_payment_terminal = fields.Selection(selection=lambda self: self._get_payment_terminal_selection(), 
                                            string='Usar Terminal de Pago', help='Registra los pagos con un terminal en este diario.')
    hide_use_payment_terminal = fields.Boolean(compute='_compute_hide_use_payment_terminal', help='Campo técnico que se utiliza para '
                                               'ocultar use_payment_terminal cuando no hay interfaces de pago instaladas.')

    @api.depends('is_cash_count')
    def _compute_hide_use_payment_terminal(self):
        no_terminals = not bool(self._fields['use_payment_terminal'].selection(self))
        for payment_method in self:
            payment_method.hide_use_payment_terminal = no_terminals or payment_method.is_cash_count

    @api.onchange('use_payment_terminal')
    def _onchange_use_payment_terminal(self):
        """Se usa heredando el modelo para desarmar el valor del campo relacionado con el terminal de pago no seleccionado."""
        pass

    @api.depends('config_ids')
    def _compute_open_session_ids(self):
        for payment_method in self:
            payment_method.open_session_ids = self.env['treasury.session'].search([('config_id', 'in', payment_method.config_ids.ids), ('state', '!=', 'closed')])

    @api.onchange('is_cash_count')
    def _onchange_is_cash_count(self):
        if not self.is_cash_count:
            self.cash_journal_id = False
        else:
            self.use_payment_terminal = False

    def _is_write_forbidden(self, fields):
        return bool(fields and self.open_session_ids)

    def write(self, vals):
        if self._is_write_forbidden(set(vals.keys())):
            raise UserError('Por favor cierre y valide las siguientes sesiones abiertas de Caja Menor antes de modificar este método de pago.\n'
                            'Sesiones Abiertas: %s' % (' '.join(self.open_session_ids.mapped('name')),))
        return super(TreasuryPaymentMethod, self).write(vals)
