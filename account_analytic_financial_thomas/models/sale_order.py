# -*- coding: utf-8 -*-
#BY: Todoo SAS - Pater

from odoo import fields,models,api
import re
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)

class SaleOrder(models.Model):
    _inherit = 'sale.order.line'

    account_id = fields.Many2one('account.account', string="Cuenta")


    @api.onchange('product_template_id')
    def _onchange_product_template_id(self):
    	if self.product_template_id:
    		self.account_id = self.product_template_id.property_account_expense_id

    
    @api.onchange('analytic_account_id')
    def onchange_analytic_account_id(self):
    	if self.product_id:
    		account_move_obj = self.env['account.account.replace'].search([('administrator_expense_account_id', '=', self.account_id.id)],limit=1)
    		if account_move_obj:
    			if self.analytic_account_id.type_type == 'op':
    				self.account_id = account_move_obj.operating_expense_account_id.id
    			elif self.analytic_account_id.type_type == 's':
    				self.account_id = account_move_obj.services_expense_account_id.id
    			elif self.analytic_account_id.type_type == 'c':
    				self.account_id = account_move_obj.business_expense_account_id.id
    			elif self.analytic_account_id.type_type == 'admin':
    				self.account_id = account_move_obj.admin_account_id.id
    	else:
     		print('No mapea cuentas')

    
    
    def _prepare_invoice_line(self):
        res = super(SaleOrder, self)._prepare_invoice_line()
        res.update({
            'account_id': self.account_id.id,
        })
        return res 				