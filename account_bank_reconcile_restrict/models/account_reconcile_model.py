from odoo import api, models


class AccountReconcileModel(models.Model):
    _inherit = "account.reconcile.model"

    def _apply_conditions(self, query, params):
        query, params = super(AccountReconcileModel, self)._apply_conditions(query, params)
        rule = self.env["account.reconcile.model"].browse(params[1])
        if rule.rule_type == "invoice_matching":
            query += ' AND account.exclude_bank_reconcile IS NOT TRUE'
        return query, params
