# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import datetime, date
from odoo.exceptions import Warning, UserError, ValidationError
import logging

class MaterialPurchaseRequisitionInherit(models.Model):
    _inherit = 'material.purchase.requisition'

    state = fields.Selection(selection_add=[
                                            ('dept_confirm', 'Aprobación 1'),
                                            ('approved', 'Aprobación 1 superada'),
                                            ('rejected', 'Aprobación 1 rechazada'),
                                            ('ir_approve', 'Aprobación 2'),
                                            ('approve', 'Aprobación 2 superada'),
                                            ('rejected2', 'Aprobación 2 rechazada'),
                                           ], tracking=True)

    code_access_groups = fields.Many2one('approvals.requisition', string="Código grupo de proceso")
    currency_id = fields.Many2one('res.currency', string='Moneda')
    is_approver = fields.Boolean(compute='_compute_check_user', readonly=True)
    is_approver2 = fields.Boolean(compute='_compute_check_user', readonly=True)


    @api.onchange('code_access_groups')
    def _compute_check_user(self):
        for record in self:
            if record.code_access_groups.approval_requisition_user_id.id == record.env.user.id:

                record.is_approver = True
            else:
                record.is_approver = False

            if record.code_access_groups.approval2_requisition_user_id.id == record.env.user.id:
                record.is_approver2 = True
            else:
                record.is_approver2 = False

                #total_cost = sum([x.total_cost for x in self.requisition_line_ids])
                #if self.code_access_groups.approval_requisition_amount > 0:
                #    if total_cost <= self.code_access_groups.approval_requisition_amount:
                #        raise ValidationError("Para superar esta etapa se debe superar el monto de: \n $"
                #                        '%s' % total_cost)
    
    
    def _check_payment_approval2(self):
        if self.state == "draft":
            active_approval = self.env['ir.config_parameter'].sudo().get_param(
                'account_payment_approval.payment_approval')
            second_approval = self.env['ir.config_parameter'].sudo().get_param(
                'account_payment_approval.approval2_user_id')
            if active_approval and second_approval and self.state == 'dept_confirm':
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
                        'state': 'ir_approve'
                    })
                    return False

        return True
    
    
    def manager_approve(self):
        res = super(MaterialPurchaseRequisitionInherit, self).manager_approve()
        if self.is_approver:
            if not self.code_access_groups.approval2_requisition_user_id:
                self.write({
                'state': 'approve'
                })
            else:
                self.write({
                    'state': 'approved'
                })

        return res

    def reject_transfer(self):
        self.write({
            'state': 'rejected'
        })
        
        
    def approve2_transfer(self):
        if self.is_approver2:
            total_cost = sum([x.total_cost for x in self.requisition_line_ids])
            if self.code_access_groups.approval2_requisition_amount > 0:
                if total_cost <= self.code_access_groups.approval2_requisition_amount:
                    raise ValidationError("Para superar esta etapa se debe superar el monto de: \n $"
                                    '%s' % total_cost)
            self.write({
                'state': 'approve'
            })

    def reject2_transfer(self):
        self.write({
            'state': 'rejected2'
        })
        
    def requisition_confirm(self):
        res = super(MaterialPurchaseRequisitionInherit, self).requisition_confirm()
        if not self.code_access_groups.approval_requisition_user_id:
            self.write({
                'state': 'ir_approve'
            })
            if not self.code_access_groups.approval2_requisition_user_id:
                self.write({
                    'state': 'approve'
                })

        return res

    def user_approve(self):
        res = super(MaterialPurchaseRequisitionInherit, self).user_approve()
        if not self.code_access_groups.approval2_requisition_user_id:
            self.write({
                'state': 'approve'
            })

        return res
