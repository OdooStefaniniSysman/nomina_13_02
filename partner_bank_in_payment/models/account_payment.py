# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import RedirectWarning, UserError, ValidationError, AccessError, Warning
import logging

_logger = logging.getLogger(__name__)


class account_payment(models.Model):
    _inherit = 'account.payment'
    
    partner_bank_id = fields.Many2one('res.partner.bank', string='Bank account', domain="[('partner_id', '=', partner_id)]")
    partner_bank = fields.Many2one('res.bank',string='Partner Bank', related='partner_bank_id.bank_id', readonly="True")
    application_number = fields.Char(string='N° Solicitud')

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        super(account_payment,self)._onchange_partner_id()
        for record in self:
            bank_ids = record.env['res.partner.bank'].search([('partner_id','=',record.partner_id.id)])
            if bank_ids and not record.partner_bank_id:
                record.partner_bank_id = bank_ids[0]
            else:
                record.partner_bank_id = False
    
    @api.model
    def default_get(self, default_fields):
        rec = super(account_payment, self).default_get(default_fields)
        active_ids = self._context.get('active_ids') or self._context.get('active_id')
        invoices = self.env['account.move'].browse(active_ids).filtered(lambda move: move.is_invoice(include_receipts=True))

        application_number = ''
        if len(invoices) == 1:
            rec.update({'application_number': invoices.application_number})
        else:
            for inv in invoices:
                if inv.application_number:
                    application_number = application_number + inv.application_number + '/'
            rec.update({'application_number': application_number})            
        return rec
    

class payment_register(models.TransientModel):
    _inherit = 'account.payment.register'

    def _prepare_payment_vals(self, invoices):
        ''' Trae el campo de application_number desde la factura al pago'''
        
        res = super(payment_register,self)._prepare_payment_vals(invoices)
        bank_ids = self.env['res.partner.bank'].search([('partner_id','=',invoices[0].commercial_partner_id.id)])
        if bank_ids and not res.get('partner_bank_id', False):
            res['partner_bank_id'] = bank_ids[0].id
        else:
            res['partner_bank_id'] = False
             
        if len(invoices) == 1:
            res.update({'application_number': invoices.application_number})
        else:
            application_number = ''
            for inv in invoices:
                if inv.application_number:
                    application_number = application_number + inv.application_number + '/'
            res.update({'application_number': application_number})
        return res


class account_batch_payment_inherit(models.Model):
    _inherit = 'account.batch.payment'
    
    @api.model
    def create(self, vals):
        res = super(account_batch_payment_inherit, self).create(vals)
        if not res.payment_ids:
            raise ValidationError('Se deben registrar líneas de pagos por lotes')
        else: 
            if not res.payment_ids.partner_bank:
                raise ValidationError('Hay líneas por lotes sin Banco de tercero y/o Cuenta Bancaria registrada')
        return res

    def write(self, vals):
        res = super(account_batch_payment_inherit, self).write(vals)
        for record in self:     
            if not record.payment_ids:
                raise ValidationError('Se deben registrar líneas de pagos por lotes')
            
        return res