# -*- coding: utf-8 -*-

from odoo import fields,models,api
import re
from odoo.exceptions import ValidationError


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    incoterms_id = fields.Many2one('account.incoterms', string="Incoterms")
    general_notes_sales = fields.Char(string="Notas")

    def _prepare_invoice_line(self):
        res = super(SaleOrderLine, self)._prepare_invoice_line()
        res['ref_comfiar'] = self.general_notes_sales or ''
        return res

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    approver_date = fields.Date(string="Fecha de aprobación de la solicitud", tracking=True)
    delivery_plan = fields.Char(string="Plan de entrega y despacho", tracking=True)
    info_to_invoice = fields.Char(string="Info para Facturar", tracking=True)
    cost_description = fields.Char(string="Descripción del costo",tracking=True)
    additional_document_reference = fields.Char(string="Referencia del doc. de recepción",tracking=True)
    additional_document = fields.Char(string="Referencia de doc. Adicional",tracking=True)
    purchase_order_date = fields.Date(string="Fecha Orden de Compra",tracking=True)
    ticket = fields.Char(string="Ticket",tracking=True)
    # dian_resolution = fields.Char(string="Resolución DIAN",tracking=True)
    # date_of_delivery = fields.Date(string="Fecha de entrega")
    period_of_service = fields.Char(string="Periodo de servicio")
    incoterms_id = fields.Many2one('account.incoterms', string="Incoterms")
    general_notes_sales = fields.Char(string="Notas")
    operation_sale_type = fields.Selection([
        ('09', 'AIU'),
        ('10','Estándar *'),
        ('20','Nota crédito que referencia una factura electrónica.'),
        ('22','Nota crédito sin referencia a facturas *'),
        ('30','Nota débito que referencia una factura electrónica'),
        ('32','Nota débito sin referencia a facturas *')], string="Tipo de Operación")
    invoice_type_code = fields.Selection([('01','Factura de Venta'),('02','Factura de Venta Exportación'),('03','Factura por Contingencia Facturador'),('04','Factura por Contingencia DIAN')],string="Tipo de Factura Electrónica")
    payment_mean_id = fields.Many2one('account.payment.mean', string="Método de pago")
    payment_mean_code_id = fields.Many2one('account.payment.mean.code', string='Medio de pago')
    # orden_ref = fields.Char(string="Orden ref.")
    ref1_comfiar = fields.Char(string="Orden de Referencia")
    aiu = fields.Char(string='AIU')
    is_einvoicing = fields.Boolean(string='Facturación electrónica activa', related='company_id.einvoicing_enabled')
    company_country = fields.Char(string="País de la compañia", related="company_id.country_id.code")
    ref_consiliation = fields.Char(string="Ref. conciliación", tracking=True)

    customer_phone = fields.Char(string="Télefono", related="partner_id.phone")
    nit = fields.Char(string="NIT", related="partner_id.vat")
    
   
    def _prepare_invoice(self):
        res = super(SaleOrder, self)._prepare_invoice()
        res.update({
            'ticket': self.ticket,
            # 'orden_ref': self.orden_ref,
            'ref1_comfiar': self.ref1_comfiar,
            'operation_type': self.operation_sale_type,
            'invoice_type_code': self.invoice_type_code,
            'info_to_invoice': self.info_to_invoice,
            'cost_description': self.cost_description,
            'period_of_service': self.period_of_service,
            'purchase_order_date': self.purchase_order_date,
            'additional_document_reference': self.additional_document_reference,
            'additional_document': self.additional_document,
            'aiu': self.aiu,
            'payment_mean_code_id': self.payment_mean_code_id.id or False,
            'res_city_id': self.res_city_id.id or False,
            'approver_date': self.approver_date,
            'delivery_plan': self.delivery_plan,
            'ref_consiliation': self.ref_consiliation,
        })
        return res
    
    @api.onchange('partner_id')
    def onchange_partner_id(self):
        res = super(SaleOrder, self).onchange_partner_id()
        if self.partner_id:
            self.update({
                'payment_mean_code_id': self.partner_id.payment_mean_code_id.id or False
            })
        return res

    @api.onchange('payment_term_id', 'date_order', 'validity_date')
    def onchange_dates(self):
        if self.payment_term_id:
            time = sum([x.days for x in self.payment_term_id.line_ids])
            if time == 0:
                payment_mean = 1
            else:
                payment_mean = 2
            self.update({
                'payment_mean_id': self.env['account.payment.mean'].search([('code','=',payment_mean)]),
            })

    

   







    
    
    
