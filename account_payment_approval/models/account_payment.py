# -*- coding: utf-8 -*-

from odoo import models, fields, _
from odoo.exceptions import UserError, ValidationError
import logging

_logger = logging.getLogger(__name__)


class AccountPayment(models.Model):
    _inherit = "account.payment"

    def _check_is_approver(self):
        approval = self.env['ir.config_parameter'].sudo().get_param(
            'account_payment_approval.payment_approval')
        approver_id = int(self.env['ir.config_parameter'].sudo().get_param(
            'account_payment_approval.approval_user_id'))
        self.is_approver = True if self.env.user.id == approver_id and approval else False
        
    def _check_is_approver2(self):
        approval = self.env['ir.config_parameter'].sudo().get_param(
            'account_payment_approval.payment_approval')
        approver_id = int(self.env['ir.config_parameter'].sudo().get_param(
            'account_payment_approval.approval2_user_id'))
        self.is_approver2 = True if self.env.user.id == approver_id and approval else False
    
    def _check_is_approver3(self):
        approval = self.env['ir.config_parameter'].sudo().get_param(
            'account_payment_approval.payment_approval')
        approver_id = int(self.env['ir.config_parameter'].sudo().get_param(
            'account_payment_approval.approval3_user_id'))
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
        return super(AccountPayment, self)._prepare_payment_moves()
        
    
    def post(self):
        """Overwrites the post() to validate the payment in the 'approved' stage too.
        Currently Odoo allows payment posting only in draft stage.
        """
        
        AccountMove = self.env['account.move'].with_context(default_type='entry')
        for rec in self:
            validation = rec._check_payment_approval()
            if validation:
                if rec.state not in ('draft', 'approved3'):
                    raise UserError(_("Only a draft or director approved payment can be posted."))

                if any(inv.state != 'posted' for inv in rec.invoice_ids):
                    raise ValidationError(_("The payment cannot be processed because the invoice is not open!"))

                # keep the name in case of a payment reset to draft
                if not rec.name:
                    # Use the right sequence to set the name
                    if rec.payment_type == 'transfer':
                        sequence_code = 'account.payment.transfer'
                    else:
                        if rec.partner_type == 'customer':
                            if rec.payment_type == 'inbound':
                                sequence_code = 'account.payment.customer.invoice'
                            if rec.payment_type == 'outbound':
                                sequence_code = 'account.payment.customer.refund'
                        if rec.partner_type == 'supplier':
                            if rec.payment_type == 'inbound':
                                sequence_code = 'account.payment.supplier.refund'
                            if rec.payment_type == 'outbound':
                                sequence_code = 'account.payment.supplier.invoice'
                    rec.name = self.env['ir.sequence'].next_by_code(sequence_code, sequence_date=rec.payment_date)
                    if not rec.name and rec.payment_type != 'transfer':
                        raise UserError(_("You have to define a sequence for %s in your company.") % (sequence_code,))

                moves = AccountMove.create(rec._prepare_payment_moves())
                moves.filtered(lambda move: move.journal_id.post_at != 'bank_rec').post()

                # Update the state / move before performing any reconciliation.
                move_name = self._get_move_name_transfer_separator().join(moves.mapped('name'))
                rec.write({'state': 'posted', 'move_name': move_name})

                if rec.payment_type in ('inbound', 'outbound'):
                    # ==== 'inbound' / 'outbound' ====
                    if rec.invoice_ids:
                        (moves[0] + rec.invoice_ids).line_ids \
                            .filtered(lambda line: not line.reconciled and line.account_id == rec.destination_account_id and not (line.account_id == line.payment_id.writeoff_account_id and line.name == line.payment_id.writeoff_label))\
                            .reconcile()
                elif rec.payment_type == 'transfer':
                    # ==== 'transfer' ====
                    moves.mapped('line_ids')\
                        .filtered(lambda line: line.account_id == rec.company_id.transfer_account_id)\
                        .reconcile()
            #res = super(AccountPayment, self).post()
            return True        
        

    def _check_payment_approval(self):
        if self.state == "draft":
            active_approval = self.env['ir.config_parameter'].sudo().get_param(
                'account_payment_approval.payment_approval')
            first_approval = self.env['ir.config_parameter'].sudo().get_param(
                'account_payment_approval.approval_user_id')
            if active_approval and first_approval:
                amount = float(self.env['ir.config_parameter'].sudo().get_param(
                    'account_payment_approval.approval_amount'))
                payment_currency_id = int(self.env['ir.config_parameter'].sudo().get_param(
                    'account_payment_approval.approval_currency_id'))
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
    
    
    
    def _check_payment_approval2(self):
        if self.state == "draft":
            active_approval = self.env['ir.config_parameter'].sudo().get_param(
                'account_payment_approval.payment_approval')
            second_approval = self.env['ir.config_parameter'].sudo().get_param(
                'account_payment_approval.approval2_user_id')
            if active_approval and second_approval and self.state == 'waiting_approval':
                amount = float(self.env['ir.config_parameter'].sudo().get_param(
                    'account_payment_approval.approval2_amount'))
                payment_currency_id = int(self.env['ir.config_parameter'].sudo().get_param(
                    'account_payment_approval.approval2_currency_id'))
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
        if self.state == "draft":
            active_approval = self.env['ir.config_parameter'].sudo().get_param(
                'account_payment_approval.payment_approval')
            third_approval = self.env['ir.config_parameter'].sudo().get_param(
                'account_payment_approval.approval3_user_id')     
            if active_approval and third_approval and self.state == 'waiting2_approval':
                amount = float(self.env['ir.config_parameter'].sudo().get_param(
                    'account_payment_approval.approval3_amount'))
                payment_currency_id = int(self.env['ir.config_parameter'].sudo().get_param(
                    'account_payment_approval.approval3_currency_id'))
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

