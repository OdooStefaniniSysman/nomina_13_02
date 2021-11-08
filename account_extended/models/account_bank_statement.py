# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class AccountBankStatementLine(models.Model):
    _inherit = 'account.bank.statement.line'


    assigned_to = fields.Selection(string='Assigned to',
        selection=[
                ('accounting', 'Accounting'),
                ('treasury', 'Treasury'),
                ('payroll', 'Payroll'),
                ('portfolio', 'Portfolio'),
                ('receivable', 'Receivable')])
    comment = fields.Char(string='Comment')
    reconciled_move_id = fields.Many2one('account.move', compute='_get_reconciled_moves', string='Reconciled move')


    @api.depends('journal_entry_ids')
    def _get_reconciled_moves(self):
        for line in self:
            move = False
            if line.journal_entry_ids and not line.reconciled_move_id:
                move = line.journal_entry_ids.move_id[0]
            line.reconciled_move_id = move


    def send_notify_assigned_to(self):
        channel = False
        statement_id = self.statement_id
        assigned_to = self.assigned_to

        if assigned_to == 'accounting':
            channel = self.env.ref("account_extended.channel_account_bank_statement_accounting")
        elif assigned_to == 'treasury':
            channel = self.env.ref("account_extended.channel_account_bank_statement_treasury")
        elif assigned_to == 'payroll':
            channel = self.env.ref("account_extended.channel_account_bank_statement_payroll")
        elif assigned_to == 'portfolio':
            channel = self.env.ref("account_extended.channel_account_bank_statement_portfolio")
        elif assigned_to == 'receivable':
            channel = self.env.ref("account_extended.channel_account_bank_statement_receivable")

        odoobot_id = self.env['ir.model.data'].xmlid_to_res_id("base.partner_root")
        subtype_id = self.env.ref("mail.mt_comment")
        body = _("The bank statement line (%s) was assigned to the group %s." % (self.name or '', assigned_to))
        body += _("\n Bank statement <a href=# data-oe-model=account.bank.statement data-oe-id=%d>%s</a>" % (statement_id.id, statement_id.name))
        if channel:
            channel.sudo().message_post(body=body, author_id=odoobot_id, message_type='comment', subtype_id=subtype_id.id)


    def write(self, values):
        result = super(AccountBankStatementLine, self).write(values)
        if values.get('assigned_to', False):
            self.send_notify_assigned_to()

        return result


    @api.model
    def create(self, values):
        result = super(AccountBankStatementLine, self).create(values)
        if values.get('assigned_to', False):
            result.send_notify_assigned_to()

        return result


#