# -*- coding: utf-8 -*-

import logging
from odoo import fields, models, api, _
from odoo.tools import float_compare
from datetime import datetime
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class AccountPayment(models.Model):
    _inherit = 'account.payment'


    sale_order_id = fields.Many2one(
        'sale.order', string='Sale Order', required=False, index=True,
        domain="[('state', '=', 'opened')]", states={'draft': [('readonly', False)]},
        readonly=True)
        
        
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4
