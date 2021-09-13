# -*- coding: utf-8 -*-
from base64 import b64encode, b64decode
from datetime import datetime
from pytz import timezone

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class PaymentTxtGeneratorWizard(models.TransientModel):
    _name = 'payment.txt.generator.wizard'
    _description = 'Txt generator'

    transmission_date = fields.Datetime(string="Transmission date",default=fields.Datetime.now)

    def generate_txt(self):
        self.ensure_one()
        txt_setting_obg = self.env['res.bank.txt_config']
        batch_payment_obj = self.env[self._context.get('active_model')]
        batch_id = batch_payment_obj.browse(self._context.get('active_id')) or False
        if not batch_id:
            raise ValidationError(_('The system does not detect the payment batch record to generate the txt file'))

        bank_id = batch_id.journal_id.bank_id or False
        if not bank_id:
            raise ValidationError(_('Bank not found'))
        txt_setting_id = txt_setting_obg.search([('bank_id','=',bank_id.id),('state','=','active')], limit=1)
        if not txt_setting_id:
            raise ValidationError(_('No txt configuration record found for bank %s') % bank_id.name)

        var_ava = self.get_var_ava(batch_id)
        txt = txt_setting_id.get_txt(batch_id, var_ava)

        batch_id.txt_filename = 'PAGO_' + \
                                batch_id.name + \
                                '_' + \
                                bank_id.name + \
                                '_' + \
                                var_ava['date_transmission'].strftime('%d-%m-%Y %H:%M:%S') + \
                                '.txt'
        batch_id.txt_file = b64encode(txt.encode('utf-8')).decode('utf-8', 'ignore')

    def get_var_ava(self, batch_payment):
        return {
            'company_name': batch_payment.journal_id.company_id.name,
            'company_street': batch_payment.journal_id.company_id.partner_id.street,
            'date_payment': batch_payment.date,
            'date_transmission': self.transmission_date.astimezone(timezone(self.env.user.tz)),
            'amount_total': sum([x.amount for x in batch_payment.payment_ids]),
            'number_lines': len(batch_payment.payment_ids),
            'dispersing_account': batch_payment.journal_id.bank_acc_number,

            'beneficiary_name': '',
            'beneficiary_street': '',
            'amount_line': '',
            'circular': '',
            'item': '',
        }    
