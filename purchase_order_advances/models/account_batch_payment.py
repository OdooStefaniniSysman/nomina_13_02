# -*- coding: utf-8 -*-

import logging
from odoo import fields, models, api, _
from odoo.tools import float_compare
from datetime import datetime
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class AccountBatchPayment(models.Model):
    _inherit = 'account.batch.payment'

    payment_as_advance = fields.Boolean(string="Payment as Advance")

    @api.onchange('payment_as_advance')
    def _onchange_payment_as_advance(self):
        for record in self:
            if record.payment_as_advance:
                record.payment_ids.write({'payment_as_advance': True,})
            else:
                record.payment_ids.write({'payment_as_advance': False,})
        
        
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4
