# -*- coding: utf-8 -*-
#BY: Todoo SAS - Pater

from odoo import fields,models,api
import re
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)

class AccountMove(models.Model):
    _inherit = 'account.move'
    

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'
    type_type = fields.Selection(string="Tipo", related="analytic_account_id.type_type")
    
    ############################################################################################
    @api.onchange('analytic_account_id','account_id')
    def onchange_analytic_account_id(self):
    	_logger.error('*****************************************pater************************************************************')
    	if self.account_id:
    		account_replace = self.env['account.account.replace'].search([('administrator_expense_account_id', '=', self.account_id.id)])
    		_logger.error('++++++++++++++++++++++++++++++++++LFPV+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
    		_logger.error(self.account_id)
    		_logger.error(account_replace)
    		if account_replace:
	    		if self.analytic_account_id.type_type == 'op':
	    			self.account_id = account_replace.operating_expense_account_id.id
	    		elif self.analytic_account_id.type_type == 's':
	    			self.account_id = account_replace.services_expense_account_id.id
	    		elif self.analytic_account_id.type_type == 'c':
	    			self.account_id = account_replace.business_expense_account_id.id
	    		elif self.analytic_account_id.type_type == 'admin':
	    			self.account_id = account_replace.admin_account_id.id	
                
	    	else:
	    	    print('No hace nada')
	    	    _logger.error('No ejecuta nada....!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
	    	    #self.account_id = account_replace.admin_account_id.id
                		  

 	
	        
              
    
    
    
   







    
    
    