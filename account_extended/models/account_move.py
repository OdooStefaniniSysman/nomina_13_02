# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountMove(models.Model):
    _inherit = 'account.move'

    def button_comparation(self):
        self.action_comparation()
        self._compute_invoice_taxes_by_group()

    def action_comparation(self):
        partner_total = {}
        for record in self:
            for line in record.invoice_line_ids:
                partner_key = str(line.partner_id.id) + '_' + str(line.product_id.concept_type_id.name)
                if partner_total.get(partner_key):
                   value = partner_total.get(partner_key)
                   value += line.price_subtotal
                   partner_total[partner_key] = value
                else:
                    partner_total[partner_key] = line.price_subtotal  
                lists = record._compute_comparation(line)
                for comparation in lists:
                    dic = {
                        'amount': line.price_subtotal,
                        'operator': comparation['comparation'],
                        'value': comparation['value']
                    }
                    if record._compute_operator(dic):
                        record.invoice_line_ids.write({'tax_ids': [(3, comparation['src'], 0)]})
                        if comparation['dest']:
                            record.invoice_line_ids.write({'tax_ids': [(4, comparation['dest'], 0)]})
                            
            for line in record.invoice_line_ids:
                partner_key = str(line.partner_id.id) + '_' + str(line.product_id.concept_type_id.name)
                lists = record._compute_comparation(line)
                for comparation in lists:
                    dic = {
                        'amount': partner_total.get(partner_key),
                        'operator': comparation['comparation'],
                        'value': comparation['value']
                    }
                    if record._compute_operator(dic):
                        record.invoice_line_ids.write({'tax_ids': [(3, comparation['src'], 0)]})
                        if comparation['dest']:
                            record.invoice_line_ids.write({'tax_ids': [(4, comparation['dest'], 0)]})                   

    def _compute_comparation(self, line):
        lists = []
        if line.partner_id.property_account_position_id:
            products = line.product_id
            ids = products.taxes_id.ids if self.type in ('out_invoice','out_refund') else products.supplier_taxes_id.ids
            type = line.product_id.concept_type_id
            lists = line.partner_id.property_account_position_id._compute_comparation(tuple(ids), type)
        return lists

    def _compute_operator(self, dic):
        amount = dic['amount']
        operator = dic['operator']
        value = dic['value']
        if operator == '==': 
            if amount == value: 
                return True 
            else: 
                return False
        elif operator == '!=':
            if amount != value:
                return True
            else: 
                return False
        elif operator == '>':
            if amount > value:
                return True
            else: 
                return False
        elif operator == '<':
            if amount < value:
                return True
            else: 
                return False    
        elif operator == '>=':
            if amount >= value:
                return True
            else: 
                return False
        elif operator == '<=':
            if amount <= value:
                return True
            else: 
                return False
        else:
            return False


    # @api.model
    # def _get_tax_grouping_key_from_tax_line(self, tax_line):
    #     return {
    #         'tax_repartition_line_id': tax_line.tax_repartition_line_id.id,
    #         'account_id': tax_line.account_id.id,
    #         'partner_id': tax_line.partner_id.id,
    #         'currency_id': tax_line.currency_id.id,
    #         'analytic_tag_ids': [(6, 0, tax_line.tax_line_id.analytic and tax_line.analytic_tag_ids.ids or [])],
    #         'analytic_account_id': tax_line.tax_line_id.analytic and tax_line.analytic_account_id.id,
    #         'tax_ids': [(6, 0, tax_line.tax_ids.ids)],
    #         'tag_ids': [(6, 0, tax_line.tag_ids.ids)],
    #     }


    # @api.model
    # def _get_tax_grouping_key_from_base_line(self, base_line, tax_vals):
    #     tax_repartition_line = self.env['account.tax.repartition.line'].browse(tax_vals['tax_repartition_line_id'])
    #     account = base_line._get_default_tax_account(tax_repartition_line) or base_line.account_id
    #     return {
    #         'tax_repartition_line_id': tax_vals['tax_repartition_line_id'],
    #         'account_id': account.id,
    #         'partner_id': base_line.partner_id.id,
    #         'currency_id': base_line.currency_id.id,
    #         'analytic_tag_ids': [(6, 0, tax_vals['analytic'] and base_line.analytic_tag_ids.ids or [])],
    #         'analytic_account_id': tax_vals['analytic'] and base_line.analytic_account_id.id,
    #         'tax_ids': [(6, 0, tax_vals['tax_ids'])],
    #         'tag_ids': [(6, 0, tax_vals['tag_ids'])],
    #     }


    # def _recompute_tax_lines(self, recompute_tax_base_amount=False):
    #     ''' Compute the dynamic tax lines of the journal entry.
    #     :param lines_map: The line_ids dispatched by type containing:
    #         * base_lines: The lines having a tax_ids set.
    #         * tax_lines: The lines having a tax_line_id set.
    #         * terms_lines: The lines generated by the payment terms of the invoice.
    #         * rounding_lines: The cash rounding lines of the invoice.
    #     '''
    #     self.ensure_one()
    #     in_draft_mode = self != self._origin

    #     def _serialize_tax_grouping_key(grouping_dict):
    #         ''' Serialize the dictionary values to be used in the taxes_map.
    #         :param grouping_dict: The values returned by '_get_tax_grouping_key_from_tax_line' or '_get_tax_grouping_key_from_base_line'.
    #         :return: A string representing the values.
    #         '''
    #         return '-'.join(str(v) for v in grouping_dict.values())

    #     def _compute_base_line_taxes(base_line):
    #         ''' Compute taxes amounts both in company currency / foreign currency as the ratio between
    #         amount_currency & balance could not be the same as the expected currency rate.
    #         The 'amount_currency' value will be set on compute_all(...)['taxes'] in multi-currency.
    #         :param base_line:   The account.move.line owning the taxes.
    #         :return:            The result of the compute_all method.
    #         '''
    #         move = base_line.move_id

    #         if move.is_invoice(include_receipts=True):
    #             handle_price_include = True
    #             sign = -1 if move.is_inbound() else 1
    #             quantity = base_line.quantity
    #             if base_line.currency_id:
    #                 price_unit_foreign_curr = sign * base_line.price_unit * (1 - (base_line.discount / 100.0))
    #                 #price_unit_comp_curr = base_line.currency_id._convert(price_unit_foreign_curr, move.company_id.currency_id, move.company_id, move.date)
    #                 price_unit_comp_curr = base_line.currency_id._convert(price_unit_foreign_curr, move.company_id.currency_id, move.company_id, move.date, round=False)
    #             else:
    #                 price_unit_foreign_curr = 0.0
    #                 price_unit_comp_curr = sign * base_line.price_unit * (1 - (base_line.discount / 100.0))
    #             tax_type = 'sale' if move.type.startswith('out_') else 'purchase'
    #             is_refund = move.type in ('out_refund', 'in_refund')
    #         else:
    #             handle_price_include = False
    #             quantity = 1.0
    #             price_unit_foreign_curr = base_line.amount_currency
    #             price_unit_comp_curr = base_line.balance
    #             tax_type = base_line.tax_ids[0].type_tax_use if base_line.tax_ids else None
    #             is_refund = (tax_type == 'sale' and base_line.debit) or (tax_type == 'purchase' and base_line.credit)

    #         balance_taxes_res = base_line.tax_ids._origin.compute_all(
    #             price_unit_comp_curr,
    #             currency=base_line.company_currency_id,
    #             quantity=quantity,
    #             product=base_line.product_id,
    #             partner=base_line.partner_id,
    #             is_refund=self.type in ('out_refund', 'in_refund'),
    #             handle_price_include=handle_price_include,
    #         )

    #         if base_line.currency_id:
    #             # Multi-currencies mode: Taxes are computed both in company's currency / foreign currency.
    #             amount_currency_taxes_res = base_line.tax_ids._origin.compute_all(
    #                 price_unit_foreign_curr,
    #                 currency=base_line.currency_id,
    #                 quantity=quantity,
    #                 product=base_line.product_id,
    #                 partner=base_line.partner_id,
    #                 is_refund=self.type in ('out_refund', 'in_refund'),
    #             )

    #             if move.type == 'entry':
    #                 repartition_field = is_refund and 'refund_repartition_line_ids' or 'invoice_repartition_line_ids'
    #                 repartition_tags = base_line.tax_ids.mapped(repartition_field).filtered(lambda x: x.repartition_type == 'base').tag_ids
    #                 tags_need_inversion = (tax_type == 'sale' and not is_refund) or (tax_type == 'purchase' and is_refund)
    #                 if tags_need_inversion:
    #                     balance_taxes_res['base_tags'] = base_line._revert_signed_tags(repartition_tags).ids
    #                     for tax_res in balance_taxes_res['taxes']:
    #                         tax_res['tag_ids'] = base_line._revert_signed_tags(self.env['account.account.tag'].browse(tax_res['tag_ids'])).ids

    #             for b_tax_res, ac_tax_res in zip(balance_taxes_res['taxes'], amount_currency_taxes_res['taxes']):
    #                 tax = self.env['account.tax'].browse(b_tax_res['id'])
    #                 b_tax_res['amount_currency'] = ac_tax_res['amount']

    #                 # A tax having a fixed amount must be converted into the company currency when dealing with a
    #                 # foreign currency.
    #                 if tax.amount_type == 'fixed':
    #                     b_tax_res['amount'] = base_line.currency_id._convert(b_tax_res['amount'], move.company_id.currency_id, move.company_id, move.date)

    #         return balance_taxes_res

    #     taxes_map = {}

    #     # ==== Add tax lines ====
    #     to_remove = self.env['account.move.line']
    #     for line in self.line_ids.filtered('tax_repartition_line_id'):
    #         grouping_dict = self._get_tax_grouping_key_from_tax_line(line)
    #         grouping_key = _serialize_tax_grouping_key(grouping_dict)
    #         if grouping_key in taxes_map:
    #             # A line with the same key does already exist, we only need one
    #             # to modify it; we have to drop this one.
    #             to_remove += line
    #         else:
    #             taxes_map[grouping_key] = {
    #                 'tax_line': line,
    #                 'balance': 0.0,
    #                 'amount_currency': 0.0,
    #                 'tax_base_amount': 0.0,
    #                 'grouping_dict': False,
    #             }
    #     self.line_ids -= to_remove

    #     # ==== Mount base lines ====
    #     #for line in self.line_ids.filtered(lambda line: not line.exclude_from_invoice_tab):
    #     for line in self.line_ids.filtered(lambda line: not line.tax_repartition_line_id):
    #         # Don't call compute_all if there is no tax.
    #         if not line.tax_ids:
    #             line.tag_ids = [(5, 0, 0)]
    #             continue

    #         compute_all_vals = _compute_base_line_taxes(line)

    #         # Assign tags on base line
    #         line.tag_ids = compute_all_vals['base_tags']

    #         tax_exigible = True
    #         for tax_vals in compute_all_vals['taxes']:
    #             grouping_dict = self._get_tax_grouping_key_from_base_line(line, tax_vals)
    #             grouping_key = _serialize_tax_grouping_key(grouping_dict)

    #             tax_repartition_line = self.env['account.tax.repartition.line'].browse(tax_vals['tax_repartition_line_id'])
    #             tax = tax_repartition_line.invoice_tax_id or tax_repartition_line.refund_tax_id

    #             if tax.tax_exigibility == 'on_payment':
    #                 tax_exigible = False

    #             taxes_map_entry = taxes_map.setdefault(grouping_key, {
    #                 'tax_line': None,
    #                 'balance': 0.0,
    #                 'amount_currency': 0.0,
    #                 'tax_base_amount': 0.0,
    #                 'grouping_dict': False,
    #             })
    #             taxes_map_entry['balance'] += tax_vals['amount']
    #             taxes_map_entry['amount_currency'] += tax_vals.get('amount_currency', 0.0)
    #             taxes_map_entry['tax_base_amount'] += self._get_base_amount_to_display(tax_vals['base'], tax_repartition_line)
    #             #taxes_map_entry['tax_base_amount'] += tax_vals['base']
    #             taxes_map_entry['grouping_dict'] = grouping_dict
    #         line.tax_exigible = tax_exigible

    #     # ==== Process taxes_map ====
    #     for taxes_map_entry in taxes_map.values():
    #         # Don't create tax lines with zero balance.
    #         if self.currency_id.is_zero(taxes_map_entry['balance']) and self.currency_id.is_zero(taxes_map_entry['amount_currency']):
    #             taxes_map_entry['grouping_dict'] = False

    #         tax_line = taxes_map_entry['tax_line']
    #         tax_base_amount = -taxes_map_entry['tax_base_amount'] if self.is_inbound() else taxes_map_entry['tax_base_amount']

    #         if not tax_line and not taxes_map_entry['grouping_dict']:
    #             continue
    #         elif tax_line and recompute_tax_base_amount:
    #             tax_line.tax_base_amount = tax_base_amount
    #         elif tax_line and not taxes_map_entry['grouping_dict']:
    #             # The tax line is no longer used, drop it.
    #             self.line_ids -= tax_line
    #         elif tax_line:
    #             tax_line.update({
    #                 'amount_currency': taxes_map_entry['amount_currency'],
    #                 'debit': taxes_map_entry['balance'] > 0.0 and taxes_map_entry['balance'] or 0.0,
    #                 'credit': taxes_map_entry['balance'] < 0.0 and -taxes_map_entry['balance'] or 0.0,
    #                 #'tax_base_amount': taxes_map_entry['tax_base_amount'],
    #                 'tax_base_amount': tax_base_amount,
    #                 #'partner_id': line.partner_id.id,
    #             })
    #         else:
    #             create_method = in_draft_mode and self.env['account.move.line'].new or self.env['account.move.line'].create
    #             tax_repartition_line_id = taxes_map_entry['grouping_dict']['tax_repartition_line_id']
    #             tax_repartition_line = self.env['account.tax.repartition.line'].browse(tax_repartition_line_id)
    #             tax = tax_repartition_line.invoice_tax_id or tax_repartition_line.refund_tax_id
    #             tax_line = create_method({
    #                 'name': tax.name,
    #                 'move_id': self.id,
    #                 'partner_id': line.partner_id.id,
    #                 'company_id': line.company_id.id,
    #                 'company_currency_id': line.company_currency_id.id,
    #                 'quantity': 1.0,
    #                 'date_maturity': False,
    #                 'amount_currency': taxes_map_entry['amount_currency'],
    #                 'debit': taxes_map_entry['balance'] > 0.0 and taxes_map_entry['balance'] or 0.0,
    #                 'credit': taxes_map_entry['balance'] < 0.0 and -taxes_map_entry['balance'] or 0.0,
    #                 'tax_base_amount': tax_base_amount,
    #                 'exclude_from_invoice_tab': True,
    #                 'tax_exigible': tax.tax_exigibility == 'on_invoice',
    #                 **taxes_map_entry['grouping_dict'],
    #             })

    #         if in_draft_mode:
    #             tax_line._onchange_amount_currency()
    #             tax_line._onchange_balance()
