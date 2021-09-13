# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountTax(models.Model):
    _inherit = 'account.tax'

    is_ica = fields.Boolean(string='Impuesto ICA', default=False)
    city_id = fields.Many2one('res.city.zip', string='Ciudad')
    # activity_ids = fields.Many2many('res.activity.ica', string='Actividades')

