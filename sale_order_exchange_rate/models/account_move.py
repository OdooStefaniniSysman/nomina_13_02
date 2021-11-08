# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountMove(models.Model):
    _inherit = 'account.move'

    sale_order_id = fields.Many2one('sale.order', 'Sale Order ID')


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4
