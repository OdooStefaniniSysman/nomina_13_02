# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
import logging

_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = "res.partner"
    
    
    property_account_advance_receivable_id = fields.Many2one('account.account', company_dependent=True,
        string="Account Advance Receivable",
        domain="[('reconcile', '=', True), ('deprecated', '=', False)]",
        help="This account will be used instead of the default one as the advance receivable account for the current partner",
        required=True)
    
    property_account_advance_payable_id = fields.Many2one('account.account', company_dependent=True,
        string="Account Advance Payable",
        domain="[('reconcile', '=', True), ('deprecated', '=', False)]",
        help="This account will be used instead of the default one as the advance payable account for the current partner",
        required=True)
    
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: