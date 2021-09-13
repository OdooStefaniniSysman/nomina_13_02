# -*- coding: utf-8 -*-

from odoo import api, fields, models

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    analytic_account_id = fields.Many2one('account.analytic.account', string='Analytic Account', ondelete='set null')
    item = fields.Integer(string='Item')

    def _prepare_invoice_line(self):
        res = super(SaleOrderLine, self)._prepare_invoice_line()
        res['analytic_account_id'] = self.analytic_account_id.id or self.order_id.analytic_account_id.id or False
        res['item'] = self.item
        return res
    