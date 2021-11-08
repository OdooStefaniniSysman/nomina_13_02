# -*- coding: utf-8 -*-

import logging
from odoo import fields, models, api, _
from odoo.tools import float_compare
from datetime import datetime
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    
    so_has_exchange_rate = fields.Boolean('Sale Order has currency exchange rate')
    so_exchange_rate = fields.Float('Currency Exchange Rate Value', default=1)
    amount_total_exchange_rate = fields.Monetary(string='Total with Exchange Rate apply', 
                                                 store=True, readonly=True, compute='_amount_all_with_exchange_rate', tracking=4)
    company_currency_id = fields.Many2one("res.currency", related='company_id.currency_id', string="Local Currency", readonly=True, required=True)
    so_exchange_allow_ok = fields.Boolean('Allow Exchange Rate', compute="_compute_so_exchange_allow")
    currency_rate_raw = fields.Float("Rate", help="Native field calc from res currency rates")
    

    @api.depends('so_has_exchange_rate','amount_total')
    def _amount_all_with_exchange_rate(self):
        for rec in self:
            if rec.so_has_exchange_rate and rec.so_exchange_rate > 1:
                rec.amount_total_exchange_rate = rec.amount_total * rec.so_exchange_rate
            elif not rec.so_has_exchange_rate and rec.currency_rate_raw > 1:
                rec.amount_total_exchange_rate = rec.amount_total * rec.currency_rate_raw
    
    @api.depends('pricelist_id', 'date_order', 'company_id','so_has_exchange_rate')
    def _compute_currency_rate(self):
        super(SaleOrder, self)._compute_currency_rate()
        for order in self:
            if order.so_has_exchange_rate and order.so_exchange_rate > 1:
                if not order.company_id:
                    order.currency_rate = 1/order.so_exchange_rate or 1.0
                    continue
                elif order.company_id.currency_id and order.currency_id:  # the following crashes if any one is undefined
                    order.currency_rate = 1/order.so_exchange_rate
                else:
                    order.currency_rate = 1.0
                self.amount_total_exchange_rate = order.amount_total * order.so_exchange_rate

    @api.depends('currency_id', 'company_currency_id', 'company_id', 'so_has_exchange_rate')
    def _compute_so_exchange_allow(self):
        self.so_exchange_allow_ok = False
        if self.currency_id != self.company_currency_id:
            self.so_exchange_allow_ok = True
            
    @api.onchange('so_exchange_rate')
    def _onchange_so_exchange_rate(self):
        if self.so_has_exchange_rate:
            self.amount_total_exchange_rate = self.amount_total * self.so_exchange_rate
            
    @api.onchange('so_has_exchange_rate')
    def _onchange_so_has_exchange_rate(self):
        if self.so_has_exchange_rate:
            self.amount_total_exchange_rate = self.amount_total * self.so_exchange_rate
        else:
            self.amount_total_exchange_rate = self.amount_total * self.currency_rate_raw

    @api.onchange('pricelist_id')
    def _onchange_pricelist_id(self):
        self.currency_rate_raw = 1/self.currency_rate if self.currency_rate > 0 else 1
        '''
        if self.pricelist_id:
            date = self._context.get('date') or datetime.today()
            self.env['res.currency.rate'].flush(['rate', 'currency_id', 'company_id', 'name'])
            query = """SELECT c.id,
                COALESCE((SELECT r.rate FROM res_currency_rate r
                    WHERE r.currency_id = c.id AND r.name <= %s
                    AND (r.company_id IS NULL OR r.company_id = %s)
                    ORDER BY r.company_id, r.name DESC
                    LIMIT 1), 1.0) AS rate
                    FROM res_currency c
                WHERE c.id = %s"""
            company_obj = self.env['res.company'].browse(self.env.company.id)
            self._cr.execute(query, (date, company_obj.id, self.pricelist_id.currency_id.id))
            currency_rates = dict(self._cr.fetchall())
            rate = currency_rates.get(self.currency_id.id) or 1.0
            self.rate = 1 / rate if rate > 0 else 1
        ''' 
        self.so_has_exchange_rate = False
        self.so_exchange_rate = 1
        self.amount_total_exchange_rate = 0

            
    def _prepare_invoice(self):
        res = super(SaleOrder, self)._prepare_invoice()
        if self.so_has_exchange_rate:
            res.update({
                'sale_order_id': self.id,
                'invoice_has_exchange_rate': True,
                'invoice_exchange_rate': self.so_exchange_rate,
            })
        return res


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4
