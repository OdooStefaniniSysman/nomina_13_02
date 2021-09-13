# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import datetime, date
from odoo.exceptions import Warning, UserError

class ApprovalsRequisition(models.Model):
    _name = 'approvals.requisition'
 
    def _get_account_manager_ids(self):
        user_ids = self.env['res.users'].search([])
        account_manager_ids = user_ids.filtered(lambda l: l.has_group('account.group_account_manager'))
        return [('id', 'in', account_manager_ids.ids)]
    
    name = fields.Char('Código de grupo de acceso')
    company_id = fields.Many2one('res.company', string='Compañía')
    model_selection = fields.Selection([('requisitions', 'Requisiciones'), ('purchase', 'Compras'),],string="Modelo para Aprobaciones")

    payment_approval = fields.Boolean('Payment Approval', config_parameter='account_payment_approval.payment_approval')

    ##APPROVALS FOR REQUISITION###

    approval_requisition_user_id = fields.Many2one('res.users', string="Analyst Approver", required=False,
                                       config_parameter='account_payment_approval.approval_user_id')
    approval_requisition_amount = fields.Float('Minimum Approval Amount')
    approval_currency_id = fields.Many2one('res.currency', string='Approval Currency',
                                           config_parameter='account_payment_approval.approval_currency_id',
                                           help="Converts the payment amount to this currency if chosen.")
    approval2_requisition_user_id = fields.Many2one('res.users', string="Coordinator Approver", required=False,
                                       config_parameter='account_payment_approval.approval2_user_id')
    approval2_requisition_amount = fields.Float('Minimum Approval Amount')

    #### APPROVALS FOR PURCHASE ####

    approval_purchase_user_id = fields.Many2one('res.users', string="Analyst Approver", required=False,
                                       config_parameter='account_payment_approval.approval_user_id')
    approval_purchase_amount = fields.Float('Maximum Approval Value')
    is_conditional = fields.Boolean(string="is conditional?")
    second_approval_purchase_user_id = fields.Many2one('res.users', string="Analyst Approver", required=False,
                                       config_parameter='account_payment_approval.approval_user_id')


    approval2_purchase_user_id = fields.Many2one('res.users', string="Analyst Approver", required=False,
                                       config_parameter='account_payment_approval.approval_user_id')
    approval2_purchase_amount = fields.Float('Maximum Approval Value')
    is_conditional_2 = fields.Boolean(string="is conditional?")
    second_approval2_purchase_user_id = fields.Many2one('res.users', string="Analyst Approver", required=False,
                                       config_parameter='account_payment_approval.approval_user_id')


    approval3_purchase_user_id = fields.Many2one('res.users', string="Analyst Approver", required=False,
                                       config_parameter='account_payment_approval.approval_user_id')
    approval3_purchase_amount = fields.Float('Maximum Approval Value')
    is_conditional_3 = fields.Boolean(string="is conditional?")
    second_approval3_purchase_user_id = fields.Many2one('res.users', string="Analyst Approver", required=False,
                                       config_parameter='account_payment_approval.approval_user_id')


    approval4_purchase_user_id = fields.Many2one('res.users', string="Analyst Approver", required=False,
                                       config_parameter='account_payment_approval.approval_user_id')
    approval4_purchase_amount = fields.Float('Maximum Approval Value')
    is_conditional_4 = fields.Boolean(string="is conditional?")
    second_approval4_purchase_user_id = fields.Many2one('res.users', string="Analyst Approver", required=False,
                                       config_parameter='account_payment_approval.approval_user_id')


    approval5_purchase_user_id = fields.Many2one('res.users', string="Analyst Approver", required=False,
                                       config_parameter='account_payment_approval.approval_user_id')
    approval5_purchase_amount = fields.Float('Maximum Approval Value')
    is_conditional_5 = fields.Boolean(string="is conditional?")
    second_approval5_purchase_user_id = fields.Many2one('res.users', string="Analyst Approver", required=False,
                                       config_parameter='account_payment_approval.approval_user_id')


    approval6_purchase_user_id = fields.Many2one('res.users', string="Analyst Approver", required=False,
                                       config_parameter='account_payment_approval.approval_user_id')
    approval6_purchase_amount = fields.Float('Maximum Approval Value')
    is_conditional_6 = fields.Boolean(string="is conditional?")
    second_approval6_purchase_user_id = fields.Many2one('res.users', string="Analyst Approver", required=False,
                                       config_parameter='account_payment_approval.approval_user_id')


    approval7_purchase_user_id = fields.Many2one('res.users', string="Analyst Approver", required=False,
                                       config_parameter='account_payment_approval.approval_user_id')
    approval7_purchase_amount = fields.Float('Maximum Approval Value')
    is_conditional_7 = fields.Boolean(string="is conditional?")
    second_approval7_purchase_user_id = fields.Many2one('res.users', string="Analyst Approver", required=False,
                                       config_parameter='account_payment_approval.approval_user_id')

    

    final_approval = fields.Selection([('to approve', '1'),
                                      ('approval2', '2'),
                                      ('approval3', '3'),
                                      ('approval4', '4'),
                                      ('approval5', '5'),
                                      ('approval6', '6'),
                                      ('approval7', '7')], string="Aprobación Final")
    
    def _get_account_manager_ids(self):
        user_ids = self.env['res.users'].search([])
        account_manager_ids = user_ids.filtered(lambda l: l.has_group('account.group_account_manager'))
        return [('id', 'in', account_manager_ids.ids)]
    
    
    
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
    