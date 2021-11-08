# -*- coding: utf-8 -*-
#BY: Todoo SAS - Pater


from odoo import fields,models,api
import re
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order.line'

    account_id = fields.Many2one('account.account', string="Cuenta")


    @api.onchange('product_id')
    def _onchange_product_id(self):   
        if self.product_id:
            self.account_id = self.product_id.product_tmpl_id.get_product_accounts()['expense'].id

    
    @api.onchange('account_analytic_id')
    def onchange_account_analytic_id(self):
        if self.product_id:
            account_move_obj = self.env['account.account.replace'].search([('administrator_expense_account_id', '=', self.account_id.id)],limit=1)
            if account_move_obj:
                if self.account_analytic_id.type_type == 'op':
                    self.account_id = account_move_obj.operating_expense_account_id.id
                elif self.account_analytic_id.type_type == 's':
                    self.account_id = account_move_obj.services_expense_account_id.id
                elif self.account_analytic_id.type_type == 'c':
                    self.account_id = account_move_obj.business_expense_account_id.id
                elif self.account_analytic_id.type_type == 'admin':
                    self.account_id = account_move_obj.admin_account_id.id
        else:
             print('No mapea cuentas')
                
                