# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResCurrency(models.Model):
    _inherit = 'res.currency'
    
    def _convert_per_document(self, from_amount, to_currency, company, date, exchange_rate, round=True):
        self, to_currency = self or to_currency, to_currency or self
        assert self, "convert amount from unknown currency"
        assert to_currency, "convert amount to unknown currency"
        assert company, "convert amount from unknown company"
        assert date, "convert amount from unknown date"
        # apply conversion rate
        if self == to_currency:
            to_amount = from_amount
        else:
            to_amount = from_amount * abs(exchange_rate) if exchange_rate else 1
            
        # apply rounding
        return to_currency.round(to_amount) if round else to_amount
    
