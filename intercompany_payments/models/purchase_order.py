# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import Warning


class purchase_order(models.Model):

    _inherit = "purchase.order"

    currency_rate_raw = fields.Float(string="TRM del dia", default=0)
    so_has_exchange_rate = fields.Boolean(string="TRM por documento", default=False)
    res_city_id = fields.Many2one('res.city', string="Sede")
    ticket = fields.Char(string="ticket")
    additional_document_reference = fields.Char(string="Referencia del doc. de recepción",tracking=True)
    additional_document = fields.Char(string="Referencia de doc. Adicional",tracking=True)
    ref1_comfiar = fields.Char(string="Orden de Referencia")
    

    def _prepare_sale_order_data(self, name, partner, company, direct_delivery_address):
        """ Generate the Sales Order values from the PO
            :param name : the origin client reference
            :rtype name : string
            :param partner : the partner reprenseting the company
            :rtype partner : res.partner record
            :param company : the company of the created SO
            :rtype company : res.company record
            :param direct_delivery_address : the address of the SO
            :rtype direct_delivery_address : res.partner record
        """
        vals = super(purchase_order, self)._prepare_sale_order_data(name, partner, company, direct_delivery_address)
        vals['currency_rate_raw'] = self.currency_rate_raw
        vals['so_has_exchange_rate'] = self.so_has_exchange_rate
        vals['res_city_id'] = self.res_city_id.id or False
        vals['ticket'] = self.ticket
        vals['incoterm'] = self.incoterm_id.id or False
        vals['additional_document_reference'] = self.additional_document_reference
        vals['additional_document'] = self.additional_document
        vals['purchase_order_date'] = self.date_order.date()
        vals['ref1_comfiar'] = self.ref1_comfiar
        return vals


    @api.model
    def _prepare_sale_order_line_data(self, line, company, sale_id):
        """ Generate the Sales Order Line values from the PO line
            :param line : the origin Purchase Order Line
            :rtype line : purchase.order.line record
            :param company : the company of the created SO
            :rtype company : res.company record
            :param sale_id : the id of the SO
        """
        # it may not affected because of parallel company relation

        vals = super(purchase_order, self)._prepare_sale_order_line_data(line, company, sale_id)
        vals['analytic_account_id'] = self.order_line.account_analytic_id.id
        return vals
