# -*- coding: utf-8 -*-

from odoo import fields, models


class AccountJournalApprovals(models.Model):
    _inherit = 'account.journal'

    def _get_account_manager_ids(self):
        user_ids = self.env['res.users'].search([])
        account_manager_ids = user_ids.filtered(lambda l: l.has_group('account.group_account_manager'))
        return [('id', 'in', account_manager_ids.ids)]
    
    payment_approval_in = fields.Boolean('Inbound Approval')
    payment_approval_out = fields.Boolean('Outbound Approval')
    
    # inbound payment approval
    approval_in_user_id = fields.Many2one(
        'res.users', 
        string="Analyst Approver", 
        required=False, 
        domain=_get_account_manager_ids
    )
    approval_in_amount = fields.Float(
        'Minimum Approval Amount',
        help="If amount is 0.00, All the payments go through approval."
    )
    approval_in_currency_id = fields.Many2one(
        'res.currency',
        string='Approval Currency',
        help="Converts the payment amount to this currency if chosen."
    )
    approval2_in_user_id = fields.Many2one(
        'res.users',
        string="Coordinator Approver",
        required=False,
        domain=_get_account_manager_ids
    )
    approval2_in_amount = fields.Float(
        'Minimum Approval Amount',
        help="If amount is 0.00, All the payments go through approval."
    )
    approval2_in_currency_id = fields.Many2one(
        'res.currency',
        string='Approval Currency',
        help="Converts the payment amount to this currency if chosen."
    )
    approval3_in_user_id = fields.Many2one(
        'res.users',
        string="Director Approver",
        required=False,
        domain=_get_account_manager_ids
    )
    approval3_in_amount = fields.Float(
        'Minimum Approval Amount',
        help="If amount is 0.00, All the payments go through approval."
    )
    approval3_in_currency_id = fields.Many2one(
        'res.currency',
        string='Approval Currency',
        help="Converts the payment amount to this currency if chosen.")
    
    # outbound payment approval
    approval_out_user_id = fields.Many2one(
        'res.users', 
        string="Analyst Approver", 
        required=False, 
        domain=_get_account_manager_ids
    )
    approval_out_amount = fields.Float(
        'Minimum Approval Amount',
        help="If amount is 0.00, All the payments go through approval."
    )
    approval_out_currency_id = fields.Many2one(
        'res.currency',
        string='Approval Currency',
        help="Converts the payment amount to this currency if chosen."
    )
    approval2_out_user_id = fields.Many2one(
        'res.users',
        string="Coordinator Approver",
        required=False,
        domain=_get_account_manager_ids
    )
    approval2_out_amount = fields.Float(
        'Minimum Approval Amount',
        help="If amount is 0.00, All the payments go through approval."
    )
    approval2_out_currency_id = fields.Many2one(
        'res.currency',
        string='Approval Currency',
        help="Converts the payment amount to this currency if chosen."
    )
    approval3_out_user_id = fields.Many2one(
        'res.users',
        string="Director Approver",
        required=False,
        domain=_get_account_manager_ids
    )
    approval3_out_amount = fields.Float(
        'Minimum Approval Amount',
        help="If amount is 0.00, All the payments go through approval."
    )
    approval3_out_currency_id = fields.Many2one(
        'res.currency',
        string='Approval Currency',
        help="Converts the payment amount to this currency if chosen.")