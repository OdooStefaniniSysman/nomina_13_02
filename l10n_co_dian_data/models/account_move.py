# -*- coding: utf-8 -*-

from odoo import api, fields, models

class AccountMove(models.Model):
    _inherit = 'account.move'

    number_contract = fields.Char(string='Contract N°')
    date_contract = fields.Date(string='Contract Date')
    additional_document_reference = fields.Char(string="Referencia del doc. de recepción",tracking=True)
    additional_document = fields.Char(string="Referencia de doc. Adicional",tracking=True)
    purchase_order_date = fields.Date(string="Fecha Orden de Compra",tracking=True)
    is_ut = fields.Boolean(string='Es unión temporal?', related='company_id.is_ut')

    @api.onchange('invoice_line_ids')
    def _onchange_invoice_line_items(self):
        if self.invoice_line_ids:
            c = 1
            for line in self.invoice_line_ids.sorted(lambda x: x.sequence):
                if not line.display_type:
                    if line.item == 0:
                        line.item = c
                    c += 1