# -*- coding: utf-8 -*-

from odoo import api, fields, models

class AccountMoveMultiCustomer(models.Model):
    _name = 'account.move.multi.customer'

    move_id = fields.Many2one('account.move', string='Factura de Venta')
    percent = fields.Float(string='Porcentaje (%)', digits=(2,2))
    partner_id = fields.Many2one('res.partner', string='Cliente')
    