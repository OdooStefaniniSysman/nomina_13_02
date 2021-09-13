# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
import base64
import json
import logging

_logger = logging.getLogger(__name__)


class AccountInvoice(models.Model):
    _inherit = "account.invoice"
        
    #este campo lo ingresa pos_universoformatucuerpo pero no aparece disponible, temporalmente me toco fijarlo directo en el módulo
    pos_order_id = fields.Many2one('pos.order', string='Orden POS', help="Relación con la Orden POS en caso que la factura tenga este origen")



