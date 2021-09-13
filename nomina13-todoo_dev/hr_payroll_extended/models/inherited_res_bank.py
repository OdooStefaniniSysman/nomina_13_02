# -*- coding: utf-8 -*-
# Copyright 2020-TODAY Miguel Pardo <ing.miguel.pardo@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from pytz import utc
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DF
from datetime import datetime
from odoo import fields, models, api, _
from odoo.tools.float_utils import float_round


class ResPartnerBank(models.Model):
    """Hr Employee."""
    _name = 'res.partner.bank' 
    _inherit = [
        'res.partner.bank', 
        'mail.thread', 'mail.activity.mixin'
    ]

    acc_type = fields.Selection(selection=lambda x: x.env['res.partner.bank'].get_supported_account_types(), compute='_compute_acc_type', string='Type', help='Bank account type: Normal or IBAN. Inferred from the bank account number.', track_visibility='onchange')
    acc_number = fields.Char('Account Number', required=True, track_visibility='onchange')
    sanitized_acc_number = fields.Char(compute='_compute_sanitized_acc_number', string='Sanitized Account Number', readonly=True, store=True, track_visibility='onchange')
    acc_holder_name = fields.Char(string='Account Holder Name', help="Account holder name, in case it is different than the name of the Account Holder", track_visibility='onchange')
    partner_id = fields.Many2one('res.partner', 'Account Holder', ondelete='cascade', index=True, track_visibility='onchange', domain=['|', ('is_company', '=', True), ('parent_id', '=', False)], required=True)
    bank_id = fields.Many2one('res.bank', string='Bank', required=True, track_visibility='onchange')
    bank_name = fields.Char(related='bank_id.name', readonly=False, track_visibility='onchange')
    bank_bic = fields.Char(related='bank_id.bic', readonly=False, track_visibility='onchange')
    sequence = fields.Integer(default=10, track_visibility='onchange')
    currency_id = fields.Many2one('res.currency', string='Currency', track_visibility='onchange')
    company_id = fields.Many2one('res.company', 'Company', default=lambda self: self.env.company, ondelete='cascade', track_visibility='onchange')
    qr_code_valid = fields.Boolean(string="Has all required arguments", compute="_validate_qr_code_arguments")

    _sql_constraints = [
        ('unique_number', 'unique(sanitized_acc_number, company_id)', 'Account Number must be unique'),
    ]


    def write(self, vals):
        if vals.get('bank_id') or vals.get('acc_number'):
            employee_id = self.env['hr.employee'].search([
                ('bank_account_id', '=', self.id)])
            if employee_id:
                if vals.get('bank_id'):
                    bank_name = self.env['res.bank'].search([
                        ('id', '=', vals.get('bank_id'))]).name
                    employee_id.message_post(
                        subject="Cambios en cuenta bancaria",
                        body=_(
                            "Los datos de la cuenta Bancaria han cambiado %s -> %s" % 
                            (self.bank_id.name, bank_name)))

                if vals.get('acc_number'):
                    employee_id.message_post(
                        subject="Cambios en cuenta bancaria",
                        body=_(
                            "Los datos de la cuenta Bancaria han cambiado %s -> %s" % 
                            (self.acc_number, vals.get('acc_number'))))
        return super(ResPartnerBank, self).write(vals)
    