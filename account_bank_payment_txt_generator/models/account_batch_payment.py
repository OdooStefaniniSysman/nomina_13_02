# -*- coding: utf-8 -*-
from base64 import b64encode, b64decode
from datetime import datetime
from pytz import timezone

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class AccountBatchPayment(models.Model):
    _inherit = 'account.batch.payment'

    payment_type = fields.Many2one('payment.type', string="Payment type")
    
    txt_filename = fields.Char(string="Name txt file")
    txt_file = fields.Binary(string="Txt file")

    def generate_txt(self):
        txt_setting_obg = self.env['res.bank.txt_config']
        for record in self:
            bank_id = record.journal_id.bank_id or False
            if not bank_id:
                raise ValidationError(_('Bank not found'))
            txt_setting_id = txt_setting_obg.search([('bank_id','=',bank_id.id),('state','=','active')], limit=1)
            if not txt_setting_id:
                raise ValidationError(_('No txt configuration record found for bank %s') % bank_id.name)
            txt = txt_setting_id.get_txt(record)
            date_txt = datetime.now(timezone(self.env.user.tz or 'GTM'))
            record.txt_filename = 'PAGO_'+ record.name + '_' + bank_id.name + '_' + date_txt.strftime('%d-%m-%Y %H:%M:%S') +'.txt'
            record.txt_file = b64encode(txt.encode('utf-8')).decode('utf-8', 'ignore')

    # def get_variables_availables(self):

    #     return {
    #         'company_name': self.journal_id.company_id.name,
    #         'company_nit': ,
    #         'company_nit_dv': ,
    #         'date_payment': ,

    #     }    
    
