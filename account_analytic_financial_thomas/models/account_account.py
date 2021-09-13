# -*- coding: utf-8 -*-
#BY: Todoo SAS - Pater

from odoo import fields,models,api
import re
from odoo.exceptions import ValidationError

class AccountAccount(models.Model):
    _inherit = 'account.account'
    type_type = fields.Selection([('s','Servicios'),('admin','Administrativo'),('c','Comercial'),('op','Operativo')], string="Tipo", tracking=True)

    operating_expense_account = fields.Many2one('account.account', string="Cuenta de gasto operativo")
    services_expense_account = fields.Many2one('account.account', string="Cuenta de gasto servicios")
    business_expense_account = fields.Many2one('account.account', string="Cuenta de gasto comercial")
    administrator_expense_account = fields.Many2one('account.account', string="Cuenta de gasto Administrativo")
    
   







    
    
    