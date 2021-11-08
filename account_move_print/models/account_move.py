# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
import base64
import json
import logging

_logger = logging.getLogger(__name__)

from . import amount_to_text

class AccountMove(models.Model):
    _inherit = "account.move"
    
    
    def _get_amount_to_text(self):
        for move in self:
            AmountText = amount_to_text.amount_to_text(self,round(move.amount))
            move.amount_to_text = AmountText
    
    amount_to_text = fields.Char(compute=_get_amount_to_text, string='Total en Texto', type="char")


