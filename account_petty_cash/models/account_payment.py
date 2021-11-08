# -*- coding: utf-8 -*-

from odoo import fields, models, api

import logging

_logger = logging.getLogger(__name__)

class AccountPayment(models.Model):
    _inherit = 'account.payment'

    treasury_session_id = fields.Many2one('treasury.session','Sesión de Caja Menor')

    @api.model
    def create(self, vals):
        res = super(AccountPayment, self).create(vals)
        if self.env.context.get('session_id'):
            session_id = self.env['treasury.session'].browse(self.env.context.get('session_id'))
            session_id.write({
                'close_payment_id': res.id,
                'state': 'paid',
            })
            res.write({'treasury_session_id': session_id.id})
        return res
    
    @api.model
    def _compute_payment_amount(self, invoices, currency, journal, date):
        res = super(AccountPayment, self)._compute_payment_amount(invoices, currency, journal, date)
        if self.env.context.get('default_amount'):
            res = self.env.context.get('default_amount')
        return res