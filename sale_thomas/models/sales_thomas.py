# -*- coding: utf-8 -*-
from itertools import groupby

from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    billing_cut = fields.Selection(string='billing cut day', related='partner_id.billing_cut_day')
    request_number = fields.Char(string='N° Request')
    
    # is_tst = fields.Boolean('is_tst', related='company_id.is_tst')

    def _prepare_invoice(self):
        res = super(SaleOrder, self)._prepare_invoice()
        res['request_number'] = self.request_number or False
        return res
    
    def _create_invoices(self, grouped=False, final=False):
        moves = super(SaleOrder, self)._create_invoices(grouped=grouped, final=final)
        for move in moves:
            if move.invoice_origin:
                sale_ids = self.env['sale.order'].search([('name','in',move.invoice_origin.split(', ')),('request_number','!=',False)])
                if len(sale_ids) > 1:
                    move.request_number = ', '.join([x.request_number for x in sale_ids])
                print('Hallo')
        return moves