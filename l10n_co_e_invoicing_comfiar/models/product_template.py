# -*- coding: utf-8 -*-
# Copyright 2019 Joan Marín <Github@JoanMarin>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api
import odoo.addons.decimal_precision as dp


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    @api.model
    def _default_product_scheme(self):
        return self.env['product.scheme'].search([('code', '=', '999' )]).id

    margin_percentage = fields.Float(
        string='Margin Percentage',
        help='The cost price + this percentage will be the reference price',
        digits=dp.get_precision('Discount'),
        default=10)
    reference_price = fields.Float(
        string='Reference Price',
        help='use this field if the reference price does not depend on the cost price',
        digits=dp.get_precision('Product Price'))
    product_scheme_id = fields.Many2one(
        comodel_name='product.scheme',
        string='Product Scheme',
        default=_default_product_scheme)
    product_scheme_code = fields.Char(string='Standard code')
    brand_name = fields.Char(string='Brand name')
    model_name = fields.Char(string='Model name')
    property_account_return_income_id = fields.Many2one('account.account', company_dependent=True,
        string="Account income return",
        domain="['&', ('deprecated', '=', False), ('company_id', '=', current_company_id)]",)

    # def _get_product_accounts(self):
    #     """ Add the stock accounts related to product to the result of super()
    #     @return: dictionary which contains information regarding stock accounts and super (income+expense accounts)
    #     """
    #     accounts = super(ProductTemplate, self)._get_product_accounts()
    #     res = self._get_asset_accounts()
    #     accounts.update({
    #         'stock_input': res['stock_input'] or self.categ_id.property_stock_account_input_categ_id,
    #         'stock_output': res['stock_output'] or self.categ_id.property_stock_account_output_categ_id,
    #         'stock_valuation': self.categ_id.property_stock_valuation_account_id or False,
    #     })
    #     return accounts
    
    