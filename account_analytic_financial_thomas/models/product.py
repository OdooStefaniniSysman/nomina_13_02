# -*- coding: utf-8 -*-
#BY: Todoo SAS - Pater

from odoo import fields,models,api
import re
from odoo.exceptions import ValidationError

class ProductTemplate(models.Model):
    _inherit = 'product.template'
    operating_expense_account = fields.Many2one('account.account', string="Cuenta de gasto operativo")
    services_expense_account = fields.Many2one('account.account', string="Cuenta de gasto servicios")
    business_expense_account = fields.Many2one('account.account', string="Cuenta de gasto comercial")
   