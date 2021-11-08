# -*- coding: utf-8 -*-

from odoo import fields, models, api


class AccountMove(models.Model):
    _inherit = 'account.move'

    treasury_payment_id = fields.Many2one('treasury.payment','Pago de Caja Menor')
    treasury_session_id = fields.Many2one('treasury.session','Sesión de Caja Menor')
    
    
class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    treasury_payment_id = fields.Many2one('treasury.payment','Pago de Caja Menor')
    treasury_session_id = fields.Many2one('treasury.session','Sesión de Caja Menor')