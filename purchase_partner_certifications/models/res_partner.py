# -*- coding: utf-8 -*-

from odoo import fields, models, api
from datetime import datetime
from dateutil import relativedelta


class ResPartner(models.Model):
    _inherit = "res.partner"

    last_payment = fields.Monetary(string="Ultimo pago", readonly=True, copy=False)
    last_payment_date = fields.Date(string="Fecha ultimo pago", readonly=True, copy=False)
    last_invoice = fields.Monetary(string="Ultima factura", readonly=True, copy=False)
    last_invoice_date = fields.Date(string="Fecha de la ultima factura", readonly=True, copy=False)
    logo_csc = fields.Binary(related="company_id.logo")

    
    

    