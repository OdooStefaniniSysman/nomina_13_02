# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
import logging

_logger = logging.getLogger(__name__)


class AccountAccount(models.Model):
    _inherit = "account.account"
    
    
    is_account_for_advance = fields.Boolean('Advance Account')
    
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: