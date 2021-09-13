# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import datetime, date
from odoo.exceptions import Warning, UserError, ValidationError
import logging

class PurchaseOrderInherit(models.Model):
    _inherit = 'purchase.order'

    READONLY_STATES = {
        "purchase": [("readonly", True)],
        "done": [("readonly", True)],
        "cancel": [("readonly", True)],
        "approved": [("readonly", True)],
        "to approve": [("readonly", True)],
        "approval2": [("readonly", True)],
        "approval3": [("readonly", True)],
        "approval4": [("readonly", True)],
        "approval5": [("readonly", True)],
        "approval6": [("readonly", True)],
        "approval7": [("readonly", True)],
        "approval_final": [("readonly", True)],
    }

    #asignacion de estados readonly
    partner_id = fields.Many2one(states=READONLY_STATES)
    partner_ref = fields.Char(states=READONLY_STATES)
    company_id = fields.Many2one(states=READONLY_STATES)
    po_has_exchange_rate = fields.Boolean(states=READONLY_STATES)
    incoterm_id = fields.Many2one(states=READONLY_STATES)


    state = fields.Selection(selection_add=[
                                            ('to approve', 'Aprobación 1'),
                                            ('approval2', 'Aprobación 2'),
                                            ('approval3', 'Aprobación 3'),
                                            ('approval4', 'Aprobación 4'),
                                            ('approval5', 'Aprobación 5'),
                                            ('approval6', 'Aprobación 6'),
                                            ('approval7', 'Aprobación 7'),
                                            ('approval_final', 'Confirmar Orden'),
                                           ], tracking=True)

    code_access_groups = fields.Many2one('approvals.requisition',compute='_relate_code_acces_requisition', string="Código grupo de proceso", store=True)
    is_approver = fields.Boolean(compute='_compute_check_user', readonly=True)
    is_approver2 = fields.Boolean(compute='_compute_check_user', readonly=True)
    is_approver2 = fields.Boolean(compute='_compute_check_user', readonly=True)
    is_approver3 = fields.Boolean(compute='_compute_check_user', readonly=True)
    is_approver4 = fields.Boolean(compute='_compute_check_user', readonly=True)
    is_approver5 = fields.Boolean(compute='_compute_check_user', readonly=True)
    is_approver6 = fields.Boolean(compute='_compute_check_user', readonly=True)
    is_approver7 = fields.Boolean(compute='_compute_check_user', readonly=True)
    check_final_approval = fields.Boolean(compute='_compute_final_approval', readonly=True)

    @api.depends('code_access_groups')
    def _relate_code_acces_requisition(self):
        for record in self:
            if record.custom_requisition_id.code_access_groups:
                record.code_access_groups = record.custom_requisition_id.code_access_groups.id
            else:
                record.code_access_groups = False

    @api.onchange('code_access_groups')
    def _compute_check_user(self):

        #total_cost = sum([x.price_subtotal for x in self.order_line])
                #if self.code_access_groups.approval_requisition_amount > 0:
                #    if total_cost <= self.code_access_groups.approval_requisition_amount:
                #        raise ValidationError("Para superar esta etapa se debe superar el monto de: \n $"
                #                        '%s' % total_cost)
        total = self.amount_untaxed if self.currency_id.name == 'COP' else self.amount_untaxed*self.currency_rate_raw

        
        for record in self:
            groups = record.code_access_groups
            
            # if record.code_access_groups.approval_purchase_user_id.id == record.env.user.id:
            #     record.is_approver = True
            # else:
            #     record.is_approver = False
            
            if groups.is_conditional:
                if total > groups.approval_purchase_amount and groups.second_approval_purchase_user_id.id == record.env.user.id:
                    record.is_approver = True 
                elif total <= groups.approval_purchase_amount and groups.approval_purchase_user_id.id == record.env.user.id:
                    record.is_approver = True 
                elif groups.approval_purchase_amount == 0 and (groups.second_approval_purchase_user_id.id == record.env.user.id or groups.approval_purchase_user_id.id == record.env.user.id):
                    record.is_approver = True 
                else:
                    record.is_approver = False 
            else:
                record.is_approver = True if (groups.approval_purchase_user_id.id == record.env.user.id) else False


            if groups.is_conditional_2:
                if total > groups.approval2_purchase_amount and groups.second_approval2_purchase_user_id.id == record.env.user.id:
                    record.is_approver2 = True 
                elif total <= groups.approval2_purchase_amount and groups.approval2_purchase_user_id.id == record.env.user.id:
                    record.is_approver2 = True 
                elif groups.approval2_purchase_amount == 0 and (groups.second_approval2_purchase_user_id.id == record.env.user.id or groups.approval2_purchase_user_id.id == record.env.user.id):
                    record.is_approver2 = True 
                else:
                    record.is_approver2 = False 
            else:
                record.is_approver2 = True if (groups.approval2_purchase_user_id.id == record.env.user.id) else False



            if groups.is_conditional_3:
                if total > groups.approval3_purchase_amount and groups.second_approval3_purchase_user_id.id == record.env.user.id:
                    record.is_approver3 = True 
                elif total <= groups.approval3_purchase_amount and groups.approval3_purchase_user_id.id == record.env.user.id:
                    record.is_approver3 = True 
                elif groups.approval3_purchase_amount == 0 and (groups.second_approval3_purchase_user_id.id == record.env.user.id or groups.approval3_purchase_user_id.id == record.env.user.id):
                    record.is_approver3 = True 
                else:
                    record.is_approver3 = False 
            else:
                record.is_approver3 = True if (groups.approval3_purchase_user_id.id == record.env.user.id) else False


            if groups.is_conditional_4:
                if total > groups.approval4_purchase_amount and groups.second_approval4_purchase_user_id.id == record.env.user.id:
                    record.is_approver4 = True 
                elif total <= groups.approval4_purchase_amount and groups.approval4_purchase_user_id.id == record.env.user.id:
                    record.is_approver4 = True 
                elif groups.approval4_purchase_amount == 0 and (groups.second_approval4_purchase_user_id.id == record.env.user.id or groups.approval4_purchase_user_id.id == record.env.user.id):
                    record.is_approver4 = True 
                else:
                    record.is_approver4 = False 
            else:
                record.is_approver4 = True if (groups.approval4_purchase_user_id.id == record.env.user.id) else False


            if groups.is_conditional_5:
                if total > groups.approval5_purchase_amount and groups.second_approval5_purchase_user_id.id == record.env.user.id:
                    record.is_approver5 = True
                elif total <= groups.approval5_purchase_amount and groups.approval5_purchase_user_id.id == record.env.user.id:
                    record.is_approver5 = True  
                elif groups.approval5_purchase_amount == 0 and (groups.second_approval5_purchase_user_id.id == record.env.user.id or groups.approval5_purchase_user_id.id == record.env.user.id):
                    record.is_approver5 = True 
                else:
                    record.is_approver5 = False 
            else:
                record.is_approver5 = True if (groups.approval5_purchase_user_id.id == record.env.user.id) else False



            if groups.is_conditional_6:
                if total > groups.approval6_purchase_amount and groups.second_approval6_purchase_user_id.id == record.env.user.id:
                    record.is_approver6 = True
                elif total <= groups.approval6_purchase_amount and groups.approval6_purchase_user_id.id == record.env.user.id:
                    record.is_approver6 = True  
                elif groups.approval6_purchase_amount == 0 and (groups.second_approval6_purchase_user_id.id == record.env.user.id or groups.approval6_purchase_user_id.id == record.env.user.id):
                    record.is_approver6 = True 
                else:
                    record.is_approver6 = False 
            else:
                record.is_approver6 = True if (groups.approval6_purchase_user_id.id == record.env.user.id) else False



            if groups.is_conditional_7:
                if total > groups.approval7_purchase_amount and groups.second_approval7_purchase_user_id.id == record.env.user.id:
                    record.is_approver7 = True
                elif total <= groups.approval7_purchase_amount and groups.approval7_purchase_user_id.id == record.env.user.id:
                    record.is_approver7 = True  
                elif groups.approval7_purchase_amount == 0 and (groups.second_approval7_purchase_user_id.id == record.env.user.id or groups.approval7_purchase_user_id.id == record.env.user.id):
                    record.is_approver7 = True 
                else:
                    record.is_approver7 = False 
            else:
                record.is_approver7 = True if (groups.approval7_purchase_user_id.id == record.env.user.id) else False
    

            # if record.code_access_groups.approval2_purchase_user_id.id == record.env.user.id:
            #     record.is_approver2 = True
            # else:
            #     record.is_approver2 = False
            
            # if record.code_access_groups.approval3_purchase_user_id.id == record.env.user.id:
            #     record.is_approver3 = True
            # else:
            #     record.is_approver3 = False

            # if record.code_access_groups.approval4_purchase_user_id.id == record.env.user.id:
            #     record.is_approver4 = True
            # else:
            #     record.is_approver4 = False

            # if record.code_access_groups.approval5_purchase_user_id.id == record.env.user.id:
            #     record.is_approver5 = True
            # else:
            #     record.is_approver5 = False

            # if record.code_access_groups.approval6_purchase_user_id.id == record.env.user.id:
            #     record.is_approver6 = True
            # else:
            #     record.is_approver6 = False

            # if record.code_access_groups.approval7_purchase_user_id.id == record.env.user.id:
            #     record.is_approver7 = True
            # else:
            #     record.is_approver7 = False

    @api.depends('code_access_groups')
    def _compute_final_approval(self):
        for record in self:
            if record.state == record.code_access_groups.final_approval and record.code_access_groups.approval7_purchase_user_id.id == record.env.user.id:
                record.check_final_approval = True
            else:
                record.check_final_approval = False

    def button_confirm(self):
        res = super(PurchaseOrderInherit, self).button_confirm()
        # self.write({
        # 'state': 'to approve'
        # })
        to_write = 'to approve'
        if not self.code_access_groups.approval_purchase_user_id:
            # self.write({
            # 'state': 'approval2'
            # })
            to_write = 'approval2'
            if not self.code_access_groups.approval2_purchase_user_id:
                # self.write({
                # 'state': 'approval3'
                # })
                to_write = 'approval3'
                if not self.code_access_groups.approval3_purchase_user_id:
                    # self.write({
                    # 'state': 'approval4'
                    # })
                    to_write = 'approval4'
                    if not self.code_access_groups.approval4_purchase_user_id:
                        # self.write({
                        # 'state': 'approval5'
                        # })
                        to_write = 'approval5'
                        if not self.code_access_groups.approval5_purchase_user_id:
                            # self.write({
                            # 'state': 'approval6'
                            # })
                            to_write = 'approval6'
                            if not self.code_access_groups.approval6_purchase_user_id:
                                # self.write({
                                # 'state': 'approval7'
                                # })
                                to_write = 'approval7'
                                if not self.code_access_groups.approval7_purchase_user_id:
                                    # self.write({
                                    # 'state': 'approval_final'
                                    # })
                                    to_write = 'approval_final'
        self.write({'state': to_write})
        return res

    def button_approve1(self):
        self.write({
        'state': 'approval2'
        })

        if not self.code_access_groups.approval2_purchase_user_id:
            self.write({
            'state': 'approval3'
            })
            if not self.code_access_groups.approval3_purchase_user_id:
                self.write({
                'state': 'approval4'
                })
                if not self.code_access_groups.approval4_purchase_user_id:
                    self.write({
                    'state': 'approval5'
                    })
                    if not self.code_access_groups.approval5_purchase_user_id:
                        self.write({
                        'state': 'approval6'
                        })
                        if not self.code_access_groups.approval6_purchase_user_id:
                            self.write({
                            'state': 'approval7'
                            })
                            if not self.code_access_groups.approval7_purchase_user_id:
                                    self.write({
                                    'state': 'approval_final'
                                    })

    def button_approve2(self):
        self.write({
        'state': 'approval3'
        })
        if not self.code_access_groups.approval3_purchase_user_id:
                self.write({
                'state': 'approval4'
                })
                if not self.code_access_groups.approval4_purchase_user_id:
                    self.write({
                    'state': 'approval5'
                    })
                    if not self.code_access_groups.approval5_purchase_user_id:
                        self.write({
                        'state': 'approval6'
                        })
                        if not self.code_access_groups.approval6_purchase_user_id:
                            self.write({
                            'state': 'approval7'
                            })
                            if not self.code_access_groups.approval7_purchase_user_id:
                                    self.write({
                                    'state': 'approval_final'
                                    })

    def button_approve3(self):
        self.write({
        'state': 'approval4'
        })
        if not self.code_access_groups.approval4_purchase_user_id:
                    self.write({
                    'state': 'approval5'
                    })
                    if not self.code_access_groups.approval5_purchase_user_id:
                        self.write({
                        'state': 'approval6'
                        })
                        if not self.code_access_groups.approval6_purchase_user_id:
                            self.write({
                            'state': 'approval7'
                            })
                            if not self.code_access_groups.approval7_purchase_user_id:
                                    self.write({
                                    'state': 'approval_final'
                                    })

    def button_approve4(self):
        self.write({
        'state': 'approval5'
        })
        if not self.code_access_groups.approval5_purchase_user_id:
                        self.write({
                        'state': 'approval6'
                        })
                        if not self.code_access_groups.approval6_purchase_user_id:
                            self.write({
                            'state': 'approval7'
                            })
                            if not self.code_access_groups.approval7_purchase_user_id:
                                    self.write({
                                    'state': 'approval_final'
                                    })

    def button_approve5(self):
        self.write({
        'state': 'approval6'
        })
        if not self.code_access_groups.approval6_purchase_user_id:
            self.write({
            'state': 'approval7'
            })
            if not self.code_access_groups.approval7_purchase_user_id:
                                    self.write({
                                    'state': 'approval_final'
                                    })

    def button_approve6(self):
        self.write({
        'state': 'approval7'
        })
        if not self.code_access_groups.approval7_purchase_user_id:
            self.write({
            'state': 'approval_final'
            })

    def button_approve7(self):
        self.write({
        'state': 'approval_final'
        })


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    READONLY_STATES = {
        "purchase": [("readonly", True)],
        "done": [("readonly", True)],
        "cancel": [("readonly", True)],
        "approved": [("readonly", True)],
        "to approve": [("readonly", True)],
        "approval2": [("readonly", True)],
        "approval3": [("readonly", True)],
        "approval4": [("readonly", True)],
        "approval5": [("readonly", True)],
        "approval6": [("readonly", True)],
        "approval7": [("readonly", True)],
        "approval_final": [("readonly", True)],
    }

    #asignacion de estados readonly
    name = fields.Text(states=READONLY_STATES)
    city_id = fields.Many2one(states=READONLY_STATES)
    account_analytic_id = fields.Many2one(states=READONLY_STATES)
    product_qty = fields.Float(states=READONLY_STATES)
    taxes_id = fields.Many2many(states=READONLY_STATES)
