# -*- coding: utf-8 -*-

from odoo import models, fields, api
import math
from odoo.exceptions import ValidationError
from datetime import datetime,date,timedelta
from odoo.osv import expression


class account_batch_payment(models.Model):
    _inherit = 'account.batch.payment'

    @api.depends('payment_ids', 'payment_ids.amount', 'journal_id')
    def _compute_amount(self):
        super(account_batch_payment, self)._compute_amount()
        for batch in self:
            company_currency = batch.journal_id.company_id.currency_id or self.env.company.currency_id
            journal_currency = batch.journal_id.currency_id or company_currency
            amount = 0
            for payment in batch.payment_ids:
                payment_currency = payment.currency_id or company_currency
                if payment_currency == journal_currency:
                    amount += payment.amount
                else:
                    amount += payment.amount_signed
            batch.amount = amount

    @api.model
    def create(self, vals):
        res = super(account_batch_payment, self).create(vals)
        if not res.payment_ids:
            raise ValidationError('Se deben registrar líneas de pagos por lotes')
        else: 
            if not res.payment_ids.partner_bank:
                raise ValidationError('Hay líneas por lotes sin Banco de tercero y/o Cuenta Bancaria registrada')
        return res

    def write(self, vals):
        res = super(account_batch_payment, self).write(vals)
        for record in self:     
            if not record.payment_ids:
                raise ValidationError('Se deben registrar líneas de pagos por lotes')
            
        return res
    
