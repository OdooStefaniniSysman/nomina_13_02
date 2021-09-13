# -*- coding: utf-8 -*-
# Copyright 2019 Joan Marín <Github@joanmarin>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, _
from odoo.exceptions import UserError, ValidationError


class AccountInvoiceLine(models.Model):
    _inherit = "account.move.line"

    ref_comfiar = fields.Char(string='Ref Comfiar')

    def _get_invoice_lines_taxes(self, tax, tax_amount, invoice_line_taxes_total):
        tax_code = tax.tax_group_id.tax_group_type_id.code
        tax_name = tax.tax_group_id.tax_group_type_id.name
        # tax_percent = '{:.2f}'.format(tax_amount)
        tax_percent = str(tax_amount)

        if tax_code not in invoice_line_taxes_total:
            invoice_line_taxes_total[tax_code] = {}
            invoice_line_taxes_total[tax_code]['total'] = 0
            invoice_line_taxes_total[tax_code]['name'] = tax_name
            invoice_line_taxes_total[tax_code]['taxes'] = {}

        if tax_percent not in invoice_line_taxes_total[tax_code]['taxes']:
            invoice_line_taxes_total[tax_code]['taxes'][tax_percent] = {}
            invoice_line_taxes_total[tax_code]['taxes'][tax_percent]['base'] = 0
            invoice_line_taxes_total[tax_code]['taxes'][tax_percent]['amount'] = 0

        invoice_line_taxes_total[tax_code]['total'] += (
            self.price_subtotal * tax_amount / 100)
        invoice_line_taxes_total[tax_code]['taxes'][tax_percent]['base'] += (
            self.price_subtotal)
        invoice_line_taxes_total[tax_code]['taxes'][tax_percent]['amount'] += (
            self.price_subtotal * tax_amount / 100)

        return invoice_line_taxes_total

    def _get_information_content_provider_party_values(self):
        return {
            'IDschemeID': False,
            'IDschemeName': False,
            'ID': False}
    
    def _get_computed_account(self):
        res = super(AccountInvoiceLine, self)._get_computed_account()
        if self.move_id.type == 'out_refund': # and self.move_id.journal_id.sale_journal_type == 'reco':
            account_reutn_reco = self.product_id.property_account_return_income_id.id or self.product_id.categ_id.property_account_return_income_categ_id.id or False
            if not account_reutn_reco:
                raise ValidationError(_('The product does not have an income reimbursement account. set it in the product or the category.'))
            return account_reutn_reco
        return res
