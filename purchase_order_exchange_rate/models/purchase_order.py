# -*- coding: utf-8 -*-

import logging
from odoo import fields, models, api, _
from odoo.tools import float_compare
from datetime import datetime
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'
    
    
    po_has_exchange_rate = fields.Boolean('Purchase Order has currency exchange rate')
    po_exchange_rate = fields.Float('Currency Exchange Rate Value', default=1)
    amount_total_exchange_rate = fields.Monetary(string='Total with Exchange Rate apply', 
                                                 store=True, readonly=True, compute='_amount_all_with_exchange_rate', tracking=4)
    company_currency_id = fields.Many2one("res.currency", related='company_id.currency_id', string="Local Currency", readonly=True, required=True)
    po_exchange_allow_ok = fields.Boolean('Allow Exchange Rate', compute="_compute_po_exchange_allow")
    currency_rate_raw = fields.Float("Rate", help="Native field calc from res currency rates")
    

    @api.depends('po_has_exchange_rate','amount_total')
    def _amount_all_with_exchange_rate(self):
        for rec in self:
            if rec.po_has_exchange_rate and rec.po_exchange_rate > 1:
                rec.amount_total_exchange_rate = rec.amount_total * rec.po_exchange_rate
            elif not rec.po_has_exchange_rate and rec.currency_rate_raw > 1:
                rec.amount_total_exchange_rate = rec.amount_total * rec.currency_rate_raw
    
    @api.depends('date_order', 'currency_id', 'company_id', 'company_id.currency_id','po_has_exchange_rate')
    def _compute_currency_rate(self):
        super(PurchaseOrder, self)._compute_currency_rate()
        for order in self:
            if order.po_has_exchange_rate and order.po_exchange_rate > 1:
                if not order.company_id:
                    order.currency_rate = 1/order.po_exchange_rate or 1.0
                    continue
                elif order.company_id.currency_id and order.currency_id:  # the following crashes if any one is undefined
                    order.currency_rate = 1/order.po_exchange_rate
                else:
                    order.currency_rate = 1.0
                self.amount_total_exchange_rate = order.amount_total * order.po_exchange_rate

    @api.depends('currency_id', 'company_currency_id', 'company_id', 'po_has_exchange_rate')
    def _compute_po_exchange_allow(self):
        self.po_exchange_allow_ok = False
        if self.currency_id != self.company_currency_id:
            self.po_exchange_allow_ok = True
            
    @api.onchange('po_exchange_rate')
    def _onchange_po_exchange_rate(self):
        if self.po_has_exchange_rate:
            self.amount_total_exchange_rate = self.amount_total * self.po_exchange_rate
            
    @api.onchange('po_has_exchange_rate')
    def _onchange_po_has_exchange_rate(self):
        if self.po_has_exchange_rate:
            self.amount_total_exchange_rate = self.amount_total * self.po_exchange_rate
        else:
            self.amount_total_exchange_rate = self.amount_total * self.currency_rate_raw

    @api.onchange('currency_id')
    def _onchange_currency_id(self):
        self.currency_rate_raw = 1/self.currency_rate if self.currency_rate > 0 else 1
        if self.currency_id:
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
            self._cr.execute(query, (date, company_obj.id, self.currency_id.id))
            currency_rates = dict(self._cr.fetchall())
            rate = currency_rates.get(self.currency_id.id) or 1.0
            self.currency_rate_raw = 1 / rate if rate > 0 else 1
        self.po_has_exchange_rate = False
        self.po_exchange_rate = 1
        self.amount_total_exchange_rate = 0

            
    def _prepare_invoice(self):
        res = super(PurchaseOrder, self)._prepare_invoice()
        if self.po_has_exchange_rate:
            res.update({
                # 'sale_order_id': self.id,
                'invoice_has_exchange_rate': True,
                'invoice_exchange_rate': self.po_exchange_rate,
            })
        return res
    
    def action_view_invoice(self):
        result = super(PurchaseOrder, self).action_view_invoice()
        if self.po_has_exchange_rate:        
            result['context']['default_invoice_has_exchange_rate'] = True
            result['context']['default_invoice_exchange_rate'] = self.po_exchange_rate
        return result


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4
