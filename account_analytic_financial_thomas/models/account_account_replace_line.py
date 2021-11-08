# -*- coding: utf-8 -*-
#BY: Todoo SAS - Pater

from odoo import fields,models,api
import re
from odoo.exceptions import ValidationError

class AccountAccountReplace(models.Model):
    _name = 'account.account.replace.line'
    _description = 'Líneas de sustitución de Cuentas'

    account_id = fields.Many2one('account.account.replace', string="Cuenta del Producto")
    operating_expense_account = fields.Many2one('account.account', string="Cuenta de gasto operativo")
    services_expense_account = fields.Many2one('account.account', string="Cuenta de gasto servicios")
    business_expense_account = fields.Many2one('account.account', string="Cuenta de gasto comercial")
    administrator_expense_account = fields.Many2one('account.account', string="Cuenta de gasto Administrativo")

