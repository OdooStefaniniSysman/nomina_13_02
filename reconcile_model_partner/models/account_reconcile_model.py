# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountReconcileModel(models.Model):
    _inherit = 'account.reconcile.model'

    partner_id = fields.Many2one('res.partner', string='Asociado')
    second_partner_id = fields.Many2one('res.partner', string='Asociado')
    