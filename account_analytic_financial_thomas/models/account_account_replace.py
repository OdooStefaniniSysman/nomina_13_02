# -*- coding: utf-8 -*-
#BY: Todoo SAS - Pater

from odoo import fields,models,api
import re
from odoo.exceptions import ValidationError

class AccountAccountReplace(models.Model):
    _name = 'account.account.replace'
    _description = 'sustitución de Cuentas'

    name = fields.Char(string="Nombre", tracking=True)
    operating_expense_account_id = fields.Many2one('account.account', string="Mapeo cuenta Operativo")
    services_expense_account_id = fields.Many2one('account.account', string="Mapeo cuenta de servicios")
    business_expense_account_id = fields.Many2one('account.account', string="Mapeo cuenta comercial/ventas")
    admin_account_id = fields.Many2one('account.account', string="Mapeo Administrativo")
    administrator_expense_account_id = fields.Many2one('account.account', string="Mapeo cuenta principal")
    account_line_ids = fields.One2many('account.account.replace.line','account_id', 'Cuentas')