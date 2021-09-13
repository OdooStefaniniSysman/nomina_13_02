# -*- coding: utf-8 -*-

from odoo import fields,models,api
import re
from odoo.exceptions import ValidationError

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'
    general_notes_sales = fields.Char(string="Notas")

class AccountMove(models.Model):
    _inherit = 'account.move'
    
    # additional_document_reference = fields.Char(string="Referencia del doc. de recepción",tracking=True)
    # additional_document = fields.Char(string="Referencia de doc. Adicional",tracking=True)
    # purchase_order_date = fields.Char(string="Fecha Orden de Compra",tracking=True)
    dian_resolution = fields.Char(string="Resolución DIAN",tracking=True)
    ticket = fields.Char(string="Ticket",tracking=True)
    period_of_service = fields.Char(string="Periodo de servicio")
    cost_description = fields.Char(string="Descripción del costo",tracking=True)
    info_to_invoice = fields.Char(string="Info para Facturar", tracking=True)
    general_notes_sales = fields.Char(string="Notas")
    # orden_ref = fields.Char(string="Orden ref.")
    res_city_id = fields.Many2one('res.city', string="Sede")

    approver_date = fields.Date(string="Fecha de aprobación de la solicitud", tracking=True)
    delivery_plan = fields.Char(string="Plan de entrega y despacho", tracking=True)
    ref_consiliation = fields.Char(string="Ref. conciliación", tracking=True)
    company_country = fields.Char(string="País de la compañia", related="company_id.country_id.code")

    customer_phone = fields.Char(string="Télefono", related="partner_id.phone")
    nit = fields.Char(string="NIT", related="partner_id.vat")
    invoice_state = fields.Selection([
        ('CM', 'CM'),
        ('FI', 'FI'),
        ('DV', 'DV')], string="Estado Factura")
