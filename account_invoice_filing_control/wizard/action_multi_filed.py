# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import datetime, timedelta
from odoo.exceptions import UserError, ValidationError
import logging

_logger = logging.getLogger(__name__)


class AccountMoveMultiFiledInternally(models.TransientModel):
    _name="account.move.multi.filed.internally"
    
    invoice_ids = fields.One2many('account.move.multi.filed.internally.invoice', 'wizard_id', 'Facturas Relacionadas', readonly=True, required=True)
    
    @api.model
    def default_get(self, fields):
        context = dict(self._context or {})
        active_model = context.get('active_model')
        active_ids = context.get('active_ids')
        invoices = self.env[active_model].browse(active_ids)
        if any(invoice.state not in ['posted'] for invoice in invoices):
            raise UserError(_("Only invoices in posted status can be marked as filed"))
        if any(invoice.type not in ['out_invoice','out_refund','in_invoice','in_refund'] for invoice in invoices):
            raise UserError(_("Only invoice type documents can be marked as filed"))
        rec = {}
        invoice_list = []
        for inv in invoices:
            invoice_list.append((0,0,{
                'invoice_id' : inv.id,
                'name': inv.name,
            }))
        rec.update({'invoice_ids':invoice_list})
        return rec
    
    def register_multi_filed_internally(self):
        for rec in self:
            context = dict(self._context or {})
            active_ids = context.get('active_ids')
            for inv in active_ids:
                invoice_obj = self.env['account.move'].browse(inv)
                if invoice_obj and invoice_obj.state == 'cancel':
                    raise UserError(_("No puede marcar como radicada facturas en estado cancelado."))
                # mark as filed
                invoice_obj.write({
                    'invoice_filed_internally': True
                })
        return True
            
            
    

class AccountMoveMultiFiledInternallyInvoice(models.TransientModel):
    _name = 'account.move.multi.filed.internally.invoice'

    wizard_id = fields.Many2one('account.move.multi.filed.internally',string='Wizard ID')
    invoice_id = fields.Integer(string="Número Factura")
    name = fields.Char(string='Número Factura')

    
class AccountMoveMultiFiledCustomer(models.TransientModel):
    _name="account.move.multi.filed.customer"
    
    invoice_ids = fields.One2many('account.move.multi.filed.customer.invoice', 'wizard_id', 'Facturas Relacionadas', readonly=True, required=True)
    
    @api.model
    def default_get(self, fields):
        context = dict(self._context or {})
        active_model = context.get('active_model')
        active_ids = context.get('active_ids')
        invoices = self.env[active_model].browse(active_ids)
        if any(invoice.state not in ['posted'] for invoice in invoices):
            raise UserError(_("Only invoices in posted status can be marked as filed"))
        if any(invoice.type not in ['out_invoice','out_refund','in_invoice','in_refund'] for invoice in invoices):
            raise UserError(_("Only invoice type documents can be marked as filed"))
        rec = {}
        invoice_list = []
        for inv in invoices:
            invoice_list.append((0,0,{
                'invoice_id' : inv.id,
                'name': inv.name,
            }))
        rec.update({'invoice_ids':invoice_list})
        return rec
    
    def register_multi_filed_customer(self):
        for rec in self:
            context = dict(self._context or {})
            active_ids = context.get('active_ids')
            for inv in active_ids:
                invoice_obj = self.env['account.move'].browse(inv)
                if invoice_obj and invoice_obj.state == 'cancel':
                    raise UserError(_("No puede marcar como radicada facturas en estado cancelado."))
                # mark as filed
                invoice_obj.write({
                    'invoice_filed_customer': True
                })
        return True
    
    
class AccountMoveMultiFiledCustomerInvoice(models.TransientModel):
    _name = 'account.move.multi.filed.customer.invoice'

    wizard_id = fields.Many2one('account.move.multi.filed.customer',string='Wizard ID')
    invoice_id = fields.Integer(string="Número Factura")
    name = fields.Char(string='Número Factura')
    
    
    
class AccountMoveMultiFiledSupplier(models.TransientModel):
    _name="account.move.multi.filed.supplier"
    
    invoice_ids = fields.One2many('account.move.multi.filed.supplier.invoice', 'wizard_id', 'Facturas Relacionadas', readonly=True, required=True)
    
    @api.model
    def default_get(self, fields):
        context = dict(self._context or {})
        active_model = context.get('active_model')
        active_ids = context.get('active_ids')
        invoices = self.env[active_model].browse(active_ids)
        if any(invoice.state not in ['posted'] for invoice in invoices):
            raise UserError(_("Only invoices in posted status can be marked as filed"))
        if any(invoice.type not in ['out_invoice','out_refund','in_invoice','in_refund'] for invoice in invoices):
            raise UserError(_("Only invoice type documents can be marked as filed"))
        rec = {}
        invoice_list = []
        for inv in invoices:
            invoice_list.append((0,0,{
                'invoice_id' : inv.id,
                'name': inv.name,
            }))
        rec.update({'invoice_ids':invoice_list})
        return rec
    
    def register_multi_filed_supplier(self):
        for rec in self:
            context = dict(self._context or {})
            active_ids = context.get('active_ids')
            for inv in active_ids:
                invoice_obj = self.env['account.move'].browse(inv)
                if invoice_obj and invoice_obj.state == 'cancel':
                    raise UserError(_("No puede marcar como radicada facturas en estado cancelado."))
                # mark as filed
                invoice_obj.write({
                    'invoice_filed_supplier': True
                })
        return True
    

class AccountMoveMultiFiledSupplierInvoice(models.TransientModel):
    _name = 'account.move.multi.filed.supplier.invoice'

    wizard_id = fields.Many2one('account.move.multi.filed.supplier',string='Wizard ID')
    invoice_id = fields.Integer(string="Número Factura")
    name = fields.Char(string='Número Factura')
    
    
class AccountMoveMultiFiledTreasury(models.TransientModel):
    _name="account.move.multi.filed.treasury"
    
    invoice_ids = fields.One2many('account.move.multi.filed.treasury.invoice', 'wizard_id', 'Facturas Relacionadas', readonly=True, required=True)
    
    @api.model
    def default_get(self, fields):
        context = dict(self._context or {})
        active_model = context.get('active_model')
        active_ids = context.get('active_ids')
        invoices = self.env[active_model].browse(active_ids)
        if any(invoice.state not in ['posted'] for invoice in invoices):
            raise UserError(_("Only invoices in posted status can be marked as filed"))
        if any(invoice.type not in ['out_invoice','out_refund','in_invoice','in_refund'] for invoice in invoices):
            raise UserError(_("Only invoice type documents can be marked as filed"))
        rec = {}
        invoice_list = []
        for inv in invoices:
            invoice_list.append((0,0,{
                'invoice_id' : inv.id,
                'name': inv.name,
            }))
        rec.update({'invoice_ids':invoice_list})
        return rec
    
    def register_multi_filed_treasury(self):
        for rec in self:
            context = dict(self._context or {})
            active_ids = context.get('active_ids')
            for inv in active_ids:
                invoice_obj = self.env['account.move'].browse(inv)
                if invoice_obj and invoice_obj.state == 'cancel':
                    raise UserError(_("No puede marcar como radicada facturas en estado cancelado."))
                # mark as filed
                invoice_obj.write({
                    'invoice_filed_treasury': True
                })
        return True
    

class AccountMoveMultiFiledTreasuryInvoice(models.TransientModel):
    _name = 'account.move.multi.filed.treasury.invoice'

    wizard_id = fields.Many2one('account.move.multi.filed.treasury',string='Wizard ID')
    invoice_id = fields.Integer(string="Número Factura")
    name = fields.Char(string='Número Factura')