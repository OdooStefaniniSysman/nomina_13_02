# -*- coding: utf-8 -*-

from odoo import fields, models


class AccountJournal(models.Model):
    _inherit = "account.journal"
    
    account_reconciliation_ids = fields.Many2many(
        relation="account_reconcile_account_journal_rel",
        comodel_name="account.account",
        string="Cuentas Excluidas de Reconciliacion",
        #domain=[("reconcile", "=", True)],
    )
    unreconciled_payment_ok = fields.Boolean('No reconciliar, solo validar pagos')
