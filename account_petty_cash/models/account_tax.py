# -*- coding: utf-8 -*-

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class AccountTax(models.Model):
    _inherit = 'account.tax'

    commission_tax_ok = fields.Boolean(string='Impuesto para Comisiones')
