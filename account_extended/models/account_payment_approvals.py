# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
import logging

_logger = logging.getLogger(__name__)


class AccountPaymentApprovals(models.Model):
    _inherit = "account.payment"

    @api.depends('journal_id')
    def _check_is_approver(self):
        if self.journal_id:
            if self.payment_type == 'inbound':
                approval = self.journal_id.payment_approval_in
                approver_id = self.journal_id.approval_in_user_id.id
                self.is_approver = True if self.env.user.id == approver_id and approval else False
            if self.payment_type == 'outbound':
                approval = self.journal_id.payment_approval_out
                approver_id = self.journal_id.approval_out_user_id.id
                self.is_approver = True if self.env.user.id == approver_id and approval else False
    
    @api.depends('journal_id')
    def _check_is_approver2(self):
        if self.journal_id:
            if self.payment_type == 'inbound':
                approval = self.journal_id.payment_approval_in
                approver_id = self.journal_id.approval2_in_user_id.id
                self.is_approver2 = True if self.env.user.id == approver_id and approval else False
            if self.payment_type == 'outbound':
                approval = self.journal_id.payment_approval_out
                approver_id = self.journal_id.approval2_out_user_id.id
                self.is_approver2 = True if self.env.user.id == approver_id and approval else False
    
    @api.depends('journal_id')
    def _check_is_approver3(self):
        if self.journal_id:
            if self.payment_type == 'inbound':
                approval = self.journal_id.payment_approval_in
                approver_id = self.journal_id.approval3_in_user_id.id
                self.is_approver3 = True if self.env.user.id == approver_id and approval else False
            if self.payment_type == 'outbound':
                approval = self.journal_id.payment_approval_out
                approver_id = self.journal_id.approval3_out_user_id.id
                self.is_approver3 = True if self.env.user.id == approver_id and approval else False

    state = fields.Selection(selection_add=[('waiting_approval', 'Waiting For Analyst Approval'),
                                            ('approved', 'Analyst Approved'),
                                            ('rejected', 'Analyst Rejected'),
                                            ('waiting_approval2', 'Waiting For Coordinator Approval'),
                                            ('approved2', 'Coordinator Approved'),
                                            ('rejected2', 'Coordinator Rejected'),
                                            ('waiting_approval3', 'Waiting For Director Approval'),
                                            ('approved3', 'Director Approved'),
                                            ('rejected3', 'Director Rejected')
                                           ], tracking=True)
    is_approver = fields.Boolean(compute=_check_is_approver, readonly=True)
    is_approver2 = fields.Boolean(compute=_check_is_approver2, readonly=True)
    is_approver3 = fields.Boolean(compute=_check_is_approver3, readonly=True)
    
    def _prepare_payment_moves(self):
        return super(AccountPaymentApprovals, self)._prepare_payment_moves()
        
    '''
    def _check_payment_approval(self):
        if self.state == "draft":
            active_approval = self.env['account.journal'].sudo().browse(self.journal_id.id).payment_approval
            first_approval = self.env['account.journal'].sudo().browse(self.journal_id.id).approval_user_id
            if active_approval and first_approval:
                amount = float(self.env['account.journal'].sudo().browse(self.journal_id.id).approval_amount)
                payment_currency_id = int(self.env['account.journal'].browse(self.journal_id.id).approval_currency_id)
                payment_amount = self.amount
                if payment_currency_id:
                    if self.currency_id and self.currency_id.id != payment_currency_id:
                        currency_id = self.env['res.currency'].browse(payment_currency_id)
                        payment_amount = self.currency_id._convert(
                            self.amount, currency_id, self.company_id,
                            self.payment_date or fields.Date.today(), round=True)
                if payment_amount > amount:
                    self.write({
                        'state': 'waiting_approval'
                    })
                    return False
        return True
    '''
    
    def _check_payment_approval2(self):
        if self.state == "draft":
            active_approval = self.env['account.journal'].sudo().browse(self.journal_id.id).payment_approval
            second_approval = self.env['account.journal'].sudo().browse(self.journal_id.id).approval2_user_id
            if active_approval and second_approval and self.state == 'waiting_approval':
                amount = float(self.env['account.journal'].sudo().browse(self.journal_id.id).approval2_amount)
                payment_currency_id = int(self.env['account.journal'].browse(self.journal_id.id).approval2_currency_id)
                payment_amount = self.amount
                if payment_currency_id:
                    if self.currency_id and self.currency_id.id != payment_currency_id:
                        currency_id = self.env['res.currency'].browse(payment_currency_id)
                        payment_amount = self.currency_id._convert(
                            self.amount, currency_id, self.company_id,
                            self.payment_date or fields.Date.today(), round=True)
                if payment_amount > amount:
                    self.write({
                        'state': 'waiting_approval2'
                    })
                    return False
        return True
    
    def _check_payment_approval3(self):
        if self.state == "draft" and self.journal_id:
            active_approval = self.env['account.journal'].sudo().browse(self.journal_id.id).payment_approval
            third_approval = self.env['account.journal'].sudo().browse(self.journal_id.id).approval3_user_id
            if active_approval and third_approval and self.state == 'waiting2_approval':
                amount = float(self.env['account.journal'].sudo().browse(self.journal_id.id).approval3_amount)
                payment_currency_id = int(self.env['account.journal'].browse(self.journal_id.id).approval3_currency_id)
                payment_amount = self.amount
                if payment_currency_id:
                    if self.currency_id and self.currency_id.id != payment_currency_id:
                        currency_id = self.env['res.currency'].browse(payment_currency_id)
                        payment_amount = self.currency_id._convert(
                            self.amount, currency_id, self.company_id,
                            self.payment_date or fields.Date.today(), round=True)
                if payment_amount > amount:
                    self.write({
                        'state': 'waiting_approval3'
                    })
                    return False
        return True

    def approve_transfer(self):
        if self.is_approver:
            self.write({
                'state': 'approved'
            })

    def reject_transfer(self):
        self.write({
            'state': 'rejected'
        })
        
    def approve2_transfer(self):
        if self.is_approver:
            self.write({
                'state': 'approved2'
            })

    def reject2_transfer(self):
        self.write({
            'state': 'rejected2'
        })
        
    def approve3_transfer(self):
        if self.is_approver:
            self.write({
                'state': 'approved3'
            })

    def reject3_transfer(self):
        self.write({
            'state': 'rejected3'
        })
