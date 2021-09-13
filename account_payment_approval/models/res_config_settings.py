# -*- coding: utf-8 -*-

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    def _get_account_manager_ids(self):
        user_ids = self.env['res.users'].search([])
        account_manager_ids = user_ids.filtered(lambda l: l.has_group('account.group_account_manager'))
        return [('id', 'in', account_manager_ids.ids)]

    payment_approval = fields.Boolean('Payment Approval', config_parameter='account_payment_approval.payment_approval')
    approval_user_id = fields.Many2one('res.users', string="Analyst Approver", required=False,
                                       domain=_get_account_manager_ids,
                                       config_parameter='account_payment_approval.approval_user_id')
    approval_amount = fields.Float('Minimum Approval Amount', config_parameter='account_payment_approval.approval_amount',
                                   help="If amount is 0.00, All the payments go through approval.")
    approval_currency_id = fields.Many2one('res.currency', string='Approval Currency',
                                           config_parameter='account_payment_approval.approval_currency_id',
                                           help="Converts the payment amount to this currency if chosen.")
    approval2_user_id = fields.Many2one('res.users', string="Coordinator Approver", required=False,
                                       domain=_get_account_manager_ids,
                                       config_parameter='account_payment_approval.approval2_user_id')
    approval2_amount = fields.Float('Minimum Approval Amount', config_parameter='account_payment_approval.approval2_amount',
                                   help="If amount is 0.00, All the payments go through approval.")
    approval2_currency_id = fields.Many2one('res.currency', string='Approval Currency',
                                           config_parameter='account_payment_approval.approval2_currency_id',
                                           help="Converts the payment amount to this currency if chosen.")
    approval3_user_id = fields.Many2one('res.users', string="Director Approver", required=False,
                                       domain=_get_account_manager_ids,
                                       config_parameter='account_payment_approval.approval3_user_id')
    approval3_amount = fields.Float('Minimum Approval Amount', config_parameter='account_payment_approval.approval3_amount',
                                   help="If amount is 0.00, All the payments go through approval.")
    approval3_currency_id = fields.Many2one('res.currency', string='Approval Currency',
                                           config_parameter='account_payment_approval.approval3_currency_id',
                                           help="Converts the payment amount to this currency if chosen.")
