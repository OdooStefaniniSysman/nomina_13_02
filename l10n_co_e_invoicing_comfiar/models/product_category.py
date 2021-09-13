# -*- coding: utf-8 -*-

from odoo import models, fields, api
import odoo.addons.decimal_precision as dp


class ProductCategory(models.Model):
    _inherit = 'product.category'

    property_account_return_income_categ_id = fields.Many2one('account.account', company_dependent=True,
        string="Account income return",
        domain="['&', ('deprecated', '=', False), ('company_id', '=', current_company_id)]",)
        # help="The expense is accounted for when a vendor bill is validated, except in anglo-saxon accounting with perpetual inventory valuation in which case the expense (Cost of Goods Sold account) is recognized at the customer invoice validation."