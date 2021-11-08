# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import datetime, timedelta
from odoo.exceptions import UserError, ValidationError
import logging

_logger = logging.getLogger(__name__)


class TreasuryPaymentMultiValidate(models.TransientModel):
    _name="treasury.payment.multi.validate"
    
    payment_ids = fields.One2many('treasury.payment.multi.validate.payment', 'wizard_id', 'Gastos Asociados', readonly=True, required=True)
    
    @api.model
    def default_get(self, fields):
        context = dict(self._context or {})
        active_model = context.get('active_model')
        active_ids = context.get('active_ids')
        payments = self.env[active_model].browse(active_ids)
        if any(payment.state not in ['draft'] for payment in payments):
            raise UserError(_("Ha seleccionado Gastos ya validados o cancelados"))

        rec = {}
        payment_list = []
        for pay in payments:
            _logger.error(pay)
            payment_list.append((0,0,{
                'payment_id' : pay.id,
                'name': pay.name if pay.name else '/',
                'amount': pay.amount,
                'partner_id': pay.partner_id.id,
                'journal_id': pay.journal_id.id,
            }))
        rec.update({'payment_ids':payment_list})
        return rec
    
    def register_treasury_payment_multi_validate(self):
        for rec in self:
            context = dict(self._context or {})
            active_ids = context.get('active_ids')
            for pay in active_ids:
                payment_obj = self.env['treasury.payment'].browse(pay)
                if payment_obj and payment_obj.state != 'draft':
                    raise UserError(_("Ha seleccionado Gastos ya validados o cancelados."))
                payment_obj.post()
        return True
        

class TreasuryPaymentMultiValidatePayment(models.TransientModel):
    _name = 'treasury.payment.multi.validate.payment'

    wizard_id = fields.Many2one('treasury.payment.multi.validate',string='Wizard ID')
    payment_id = fields.Integer(string="ID Gasto")
    name = fields.Char(string='Número Gasto')
    amount = fields.Float(string='Valor')
    partner_id = fields.Many2one('res.partner', string='Tercero')
    journal_id = fields.Many2one('account.journal', string='Diario')
