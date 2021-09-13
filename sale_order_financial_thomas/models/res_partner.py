# -*- coding: utf-8 -*-

from odoo import fields,models,api
from odoo.exceptions import ValidationError

class ResPartner(models.Model):
    _inherit = 'res.partner'
    
    payment_mean_code_id = fields.Many2one('account.payment.mean.code', string='Medio de pago')