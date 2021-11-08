# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from odoo.tools import float_is_zero, float_compare
from datetime import datetime
from odoo.exceptions import UserError


class HrExpense(models.Model):
    _inherit = 'hr.expense'

    session_id = fields.Many2one(
        'treasury.session', 
        string='Sesión', 
        required=True, 
        index=True,
        #company_dependent=True,
        domain="[('state', '=', 'opened')]", 
        states={'draft': [('readonly', False)]},
        readonly=True)
    config_id = fields.Many2one('treasury.config', related='session_id.config_id', string="Punto de Venta", readonly=False)
    
    
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4
