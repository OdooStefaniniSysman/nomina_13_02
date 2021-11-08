# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import RedirectWarning, UserError, ValidationError, AccessError

from collections import defaultdict

MAP_INVOICE_TYPE_PARTNER_TYPE = {
    'out_invoice': 'customer',
    'out_refund': 'customer',
    'out_receipt': 'customer',
    'in_invoice': 'supplier',
    'in_refund': 'supplier',
    'in_receipt': 'supplier',
}
import logging

_logger = logging.getLogger(__name__)


class AccountPayment(models.Model):
    _inherit = 'account.payment'
    
    payment_as_advance = fields.Boolean('Payment as Advance')
    advance_account_id = fields.Many2one('account.account', 'Advance Account',
                                         domain="[('is_account_for_advance', '=', True),('reconcile', '=', True)]",
                                         help='Specify if the default account does not appear with the correct value')
    advance_assigned_ok = fields.Boolean('Advance has been allocated', help='True if the advance has been allocated')
    
    move_id = fields.Many2one('account.move', 'Account Move',
                                         help='Specify the account move ID asigned while post payment')
    
    
    @api.depends('invoice_ids', 'payment_type', 'partner_type', 'partner_id','payment_as_advance')
    def _compute_destination_account_id(self):
        super(AccountPayment, self)._compute_destination_account_id()
        for payment in self:
            if payment.payment_as_advance:
                if payment.partner_id:
                    partner = payment.partner_id.with_context(force_company=payment.company_id.id)
                    if payment.partner_type == 'customer':
                        payment.destination_account_id = partner.property_account_advance_payable_id.id
                    else:
                        payment.destination_account_id = partner.property_account_advance_receivable_id.id
                elif payment.partner_type == 'customer':
                    default_account = self.env['ir.property'].with_context(
                        force_company=payment.company_id.id).get(
                            'property_account_advance_payable_id', 'res.partner'
                        )
                    if not default_account:
                        raise ValidationError(_
                            ("There is no default advance payable account configured. You can do it from company's properties in technical configuration")
                        )
                    payment.destination_account_id = default_account.id if default_account else payment.destination_account_id
                    
                elif payment.partner_type == 'supplier':
                    default_account = self.env['ir.property'].with_context(
                        force_company=payment.company_id.id).get(
                            'property_account_advance_receivable_id', 'res.partner'
                        )
                    if not default_account:
                        raise ValidationError(_
                            ("There is no default advance receivable account configured. You can do it from company's properties in technical configuration")
                        )
                    payment.destination_account_id = default_account.id if default_account else payment.destination_account_id
                    
            # use advance account field        
            if payment.payment_as_advance and payment.advance_account_id:
                payment.destination_account_id = payment.advance_account_id

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: