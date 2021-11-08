# -*- coding: utf-8 -*-
#BY: Todoo SAS - Pater

from odoo import fields,models,api
import re
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)

    
class AccountTax(models.Model):
    _inherit = 'account.tax'

    check_max_value = fields.Boolean(string="Mayor Valor")