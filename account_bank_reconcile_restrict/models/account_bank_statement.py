# -*- coding: utf-8 -*-

from odoo import api, models, fields

class AccountBankStatementLine(models.Model):
    _inherit = "account.bank.statement.line"

    def _prepare_payment_vals(self, total):
        res = super(AccountBankStatementLine, self)._prepare_payment_vals(total)
        if self.journal_id.unreconciled_payment_ok:
            res.update({'state': 'posted',})
            if res['partner_type'] == 'customer':
                if res['payment_type'] == 'inbound':
                    sequence_code = 'account.payment.customer.invoice'
                if res['payment_type'] == 'outbound':
                        sequence_code = 'account.payment.customer.refund'
            if res['partner_type'] == 'supplier':
                if res['payment_type'] == 'inbound':
                    sequence_code = 'account.payment.supplier.refund'
                if res['payment_type'] == 'outbound':
                    sequence_code = 'account.payment.supplier.invoice'
            res['name'] = self.env['ir.sequence'].next_by_code(sequence_code, sequence_date=res['payment_date'])
        return res

    def _prepare_reconciliation_move_line(self, move, amount):
        res = super(AccountBankStatementLine, self)._prepare_reconciliation_move_line(move, amount)
        if self.journal_id.unreconciled_payment_ok:
            res.update({'statement_line_id': ''})
        return res
