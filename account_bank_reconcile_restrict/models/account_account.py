# -*- coding: utf-8 -*-

from odoo import fields, models


class AccountAccount(models.Model):
    _inherit = "account.account"

    exclude_bank_reconcile = fields.Boolean(
        string='Excluir de Reconciliacion Bancaria')
    
