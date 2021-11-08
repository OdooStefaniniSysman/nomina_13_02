# -*- coding: utf-8 -*-
#BY: Todoo SAS - Pater

from odoo import fields,models,api
import re
from odoo.exceptions import ValidationError

class AccountAnalyticAccount(models.Model):
    _inherit = 'account.analytic.account'
    type_type = fields.Selection([('s','Servicios'),('admin','Administrativo'),('c','Comercial'),('op','Operativo')], string="Tipo", tracking=True)
    
   







    
    
    