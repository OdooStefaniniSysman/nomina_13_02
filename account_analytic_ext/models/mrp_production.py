# -*- coding: utf-8 -*-

from odoo import fields, models


class MrpProduction(models.Model):
    _inherit = "mrp.production"

    analytic_account_id = fields.Many2one(
        comodel_name="account.analytic.account", string="Analytic Account"
    )
