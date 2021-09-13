# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import RedirectWarning, UserError, ValidationError, AccessError
from odoo.tools import float_is_zero, float_compare, safe_eval, date_utils, email_split, email_escape_char, email_re
from odoo.tools.misc import formatLang, format_date, get_lang

from datetime import date, timedelta
from itertools import groupby
from itertools import zip_longest
from hashlib import sha256
from json import dumps

import json
import re

class AccountPaymentInherit(models.Model):
    _inherit = 'account.payment'

    block_button_payment = fields.Boolean('Bloqueo', compute = "_compute_boolean_block")

    def action_register_payment(self):
        res = super(AccountPaymentInherit, self).action_register_payment()
        account_ids = self._context.get('active_ids')
        account_move_objs = self.env['account.move'].browse(account_ids)
        for account_move in account_move_objs:
            if account_move.block_button_payment == True:
                raise ValidationError("Para realizar el pago es necesario desbloquear la factura: \n"
                                      '%s' % account_move.name)

        return res

class AccountMoveRef(models.Model):
    _inherit = 'account.move'


    check_create_red = fields.Boolean('Check referencia', compute='_compute_check_reference')
    ref_copy = fields.Char('Referencia', readonly=True, related = 'ref')
    # state = fields.Selection(selection_add=[('blocked', 'Bloqueado'),('cancel',)])
    year_integer = fields.Integer('Año', compute="_compute_only_year", store = True)
    month_text = fields.Char('Mes', compute="_compute_month_text", store = True)
    total_documents = fields.Integer('Total de documentos', compute ='_compute_total_doc_record')
    total_recods = fields.Integer('Total de registros', compute = '_compute_total_doc_record')
    department = fields.Char('Departamento', compute="_compute_department", store = True)
    block_button_payment = fields.Boolean(string='Bloquear botón de pagos', default=False)
    
    @api.depends('create_uid')
    def _compute_department(self):
        for record in self:
            if record.create_uid.employee_id.department_id:
                record.department = record.create_uid.employee_id.department_id.name
            else:
                record.department = False
    
    @api.depends('date')
    def _compute_only_year(self):
        for record in self:
            record.year_integer = record.date.year

    @api.depends('date')
    def _compute_month_text(self):
        for record in self:
            if record.date.month == 1:
                record.month_text = 'Enero'
            elif record.date.month == 2:
                record.month_text = 'Febrero'
            elif record.date.month == 3:
                record.month_text = 'Marzo'
            elif record.date.month == 4:
                record.month_text = 'Abril'
            elif record.date.month == 5:
                record.month_text = 'Mayo'
            elif record.date.month == 6:
                record.month_text = 'Junio'
            elif record.date.month == 7:
                record.month_text = 'Julio'
            elif record.date.month == 8:
                record.month_text = 'Agosto'
            elif record.date.month == 9:
                record.month_text = 'Septiembre'
            elif record.date.month == 10:
                record.month_text = 'Octubre'
            elif record.date.month == 11:
                record.month_text = 'Noviembre'
            elif record.date.month == 12:
                record.month_text = 'Diciembre'
    
    
    @api.depends('journal_id')
    def _compute_total_doc_record(self):

        for record in self:
            documents = self.env['account.move'].search([('create_uid','=',record.create_uid.id)])
            if record.journal_id:
                record.total_documents = len(documents)
                record.total_recods = len(documents.invoice_line_ids)

    @api.model
    def create(self, vals):
        if 'ref' in vals:
            if vals['ref']:
                leads = self.env['account.move'].search([('ref_copy', '=', vals['ref'])])
                if leads:
                    vals.update(ref_copy=False)
                    # raise ValidationError("La referencia ya existe")
        res = super(AccountMoveRef, self).create(vals)
        return res
    
    def _compute_check_reference(self):
        for record in self:
            if record.ref:
                record.check_create_red = True
            else:
                record.check_create_red = False

    def post(self):
        for record in self:
            if record.type in ('in_invoice', 'in_refund'):
                record.block_button_payment = True
        return super(AccountMoveRef, self).post()

    # def action_post_block(self):
    #     for record in self:
    #         record.action_post()
    #         record.state = 'blocked'
    

    def unblock(self):
        invoices_no_block=[]
        for record in self:
            if record.block_button_payment:
                record.block_button_payment = False
            else:
                invoices_no_block += ''.join(record.name).split(',')

        if invoices_no_block:
            raise ValidationError("La(s) siguiente(s) factura(s) deben estar bloqueadas para pago:\n "
                                    '%s' % invoices_no_block)