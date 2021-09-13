# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    number_contract = fields.Char(string='Contract N°')
    date_contract = fields.Date(string='Contract Date')
    is_ut = fields.Boolean(string='Es unión temporal?', related='company_id.is_ut')
    
    def _prepare_invoice(self):
        res = super(SaleOrder, self)._prepare_invoice()
        res['number_contract'] = self.number_contract or ''
        res['date_contract'] = self.date_contract or ''
        return res
    
    def _create_invoices(self, grouped=False, final=False):
        grouped = self._context.get('grouped_sale_partner', False)
        res = super(SaleOrder, self)._create_invoices(grouped=grouped, final=final)
        for move in res:
            move._onchange_invoice_dates()
        return res

    @api.onchange('order_line')
    def _onchange_sale_line_items(self):
        if self.order_line:
            c = 1
            for line in self.order_line.sorted(lambda x: x.sequence):
                if not line.display_type:
                    if line.item == 0:
                        line.item = c
                    c += 1