# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import RedirectWarning, UserError, ValidationError, AccessError, Warning
import logging

_logger = logging.getLogger(__name__)


class AccountInvoice(models.Model):
    _inherit = 'account.move'

    invoice_filed_internally = fields.Boolean('Radicado Cartera', domain=[('type','in',['out_invoice','out_refund'])])
    invoice_filed_customer = fields.Boolean('Radicado Cliente', domain=[('type','in',['out_invoice','out_refund'])])
    
    invoice_filed_treasury = fields.Boolean('Radicaro Tesoreria', domain=[('type','in',['in_invoice','in_refund'])])
    invoice_filed_supplier = fields.Boolean('Radicado CxP', domain=[('type','in',['in_invoice','in_refund'])])
    
    def button_draft(self):
        for move in self:
            if move.invoice_filed_internally \
            or move.invoice_filed_customer \
            or move.invoice_filed_treasury \
            or move.invoice_filed_supplier:
                raise UserError(_('Cannot draft document when marked as filed'))
        super(AccountInvoice,self).button_draft()
        
