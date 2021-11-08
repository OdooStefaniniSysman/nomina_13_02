# -*- coding: utf-8 -*-

import logging
from odoo import fields, models, api, _
from odoo.tools import float_compare
from datetime import datetime
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    payment_ids = fields.One2many(
		comodel_name='account.payment',
		inverse_name='sale_order_id',
		string='Anticipos',
		domain = "[('partner_id','=',partner_id),('payment_type','=','inbound')]",
	)
    #authorize_without_advance = fields.Boolean('Authorize Advances', 
    #    groups='sale_order_advances.advances_authorized_group_user')
    authorize_without_advance = fields.Boolean('Authorize Advances') 
    
    advance_required = fields.Boolean(
        string = 'Advance Required',
        default=lambda self: self.env.user.company_id.sale_order_advance_required,
    )
    
    advance_required_percentage = fields.Float(
        string = "Percentage of Advance Required for Sales",
        default=lambda self: self.env.user.company_id.sale_order_advance_required_percentage,
    )
    
    #@api.onchange('payment_ids')
    #def _onchange_payment_ids(self):
    #    for order in self:
    #        if not order.partner_id:
    #            raise UserError(_("Debe seleccionar un cliente en la orden de venta antes de poder realizar un anticipo"))

    def _action_confirm(self):
        res = super(SaleOrder, self)._action_confirm()
        for order in self:
            advance_required = self.advance_required
            advance_required_percentage = self.advance_required_percentage
            total_advances = sum(
                payment.amount 
                for payment in order.payment_ids
                    #.mapped(state)
                    .filtered(lambda x: x.state == 'posted')
            )
            if advance_required \
                and advance_required_percentage > 0 \
                and (not total_advances or total_advances < (order.amount_total * advance_required_percentage / 100)):
                raise UserError(_("The sale order must have a minimum advance of %s percentage") 
                                % (advance_required_percentage))
            for draft_state in order.payment_ids.filtered(lambda x: x.state == 'draft'):
                if draft_state:
                    raise UserError(_("Advances must be in validated status before confirming"))
        return res
        
    def action_draft(self):
        for payment in self.payment_ids:
            payment.write({'sale_order_id': False})
        return super(SaleOrder, self).action_draft()

    def action_cancel(self):
        for payment in self.payment_ids:
            payment.write({'sale_order_id': False})
        return super(SaleOrder, self).action_cancel()


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4
