# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from odoo.exceptions import UserError


class AccountBankStatement(models.Model):
    _inherit = 'account.bank.statement'

    treasury_session_id = fields.Many2one('treasury.session', string="Sesión", copy=False)
    account_id = fields.Many2one('account.account', related='journal_id.default_debit_account_id', readonly=True)

    def check_confirm_bank(self):
        for bs in self:
            if bs.treasury_session_id.state  in ('opened', 'closing_control') and bs.state == 'open':
                raise UserError(_("No puede validar un extracto bancario que se utiliza en una sesión abierta de caja menor."))
        return super( AccountBankStatement, self).check_confirm_bank()


class AccountBankStatementLine(models.Model):
    _inherit = 'account.bank.statement.line'

    treasury_statement_id = fields.Many2one('sale.order', string="Estado de Caja Menor", ondelete='cascade')
