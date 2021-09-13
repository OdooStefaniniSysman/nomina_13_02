# -*- coding: utf-8 -*-
#BY: Todoo SAS - Pater

from odoo import fields,models,api
import re
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)

    
class AccountAsset(models.Model):
    _inherit = 'account.asset'
    
    ###########################################################################################
    @api.onchange('account_analytic_id')
    def onchange_analytic_account_id(self):
    	_logger.error('*****************************************pater asset************************************************************')
    	for rec in self:
	    	if rec.account_depreciation_expense_id:
	    		account_replace = rec.env['account.account.replace'].search([('administrator_expense_account_id', '=', rec.account_depreciation_expense_id.id)])
	    		_logger.error('++++++++++++++++++++++++++++++++++asset-LFPV+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
	    		_logger.error(rec.account_depreciation_expense_id)
	    		_logger.error(account_replace)
	    		if account_replace:
		    		if rec.account_analytic_id.type_type == 'op':
		    			rec.account_depreciation_expense_id = account_replace.operating_expense_account_id.id
		    		elif rec.account_analytic_id.type_type == 's':
		    			rec.account_depreciation_expense_id = account_replace.services_expense_account_id.id
		    		elif rec.account_analytic_id.type_type == 'c':
		    			rec.account_depreciation_expense_id = account_replace.business_expense_account_id.id
		    	else:
		    	    print('No hace nada')
     
    
    @api.onchange('account_analytic_id')
    def onchange_analytic_account_id_niff(self):
    	_logger.error('*****************************************pater asset************************************************************')
    	for rec in self:
	    	if rec.account_depreciation_expense_id_niff:
	    		account_replace = rec.env['account.account.replace'].search([('administrator_expense_account_id', '=', rec.account_depreciation_expense_id_niff.id)])
	    		_logger.error('++++++++++++++++++++++++++++++++++asset-LFPV+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
	    		_logger.error(rec.account_depreciation_expense_id_niff)
	    		_logger.error(account_replace)
	    		if account_replace:
		    		if rec.account_analytic_id.type_type == 'op':
		    			rec.account_depreciation_expense_id_niff = account_replace.operating_expense_account_id.id
		    		elif rec.account_analytic_id.type_type == 's':
		    			rec.account_depreciation_expense_id_niff = account_replace.services_expense_account_id.id
		    		elif rec.account_analytic_id.type_type == 'c':
		    			rec.account_depreciation_expense_id_niff = account_replace.business_expense_account_id.id
		    	else:
		    	    print('No hace nada')



	



		    	        	    	