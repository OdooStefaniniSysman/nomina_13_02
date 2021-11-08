# -*- coding: utf-8 -*-

from odoo import fields, models, api

'''
class AccountJournalBankCommission(models.Model):
	_name = 'account.journal.bank.commission'
    _description = "Commission "

	journal_bank_id = fields.Many2one('account.journal',string='Método de Pago') 
	journal_payment_method_id = fields.Many2one('account.journal',string='Método de Pago')
	amount_percent = fields.Float(string='Porcentaje de Comisión')
'''

class AccountJournal(models.Model):
    _inherit = 'account.journal'

    partner_id = fields.Many2one('res.partner',string='Tercero')
    petty_cash_ok = fields.Boolean(string='Permitido como Caja Menor?')
    #type = fields.Selection(selection_add=[('petty_cash', 'Petty Cash'),], tracking=True)
    
    
    #bank_base_tax_id = fields.Many2one('account.tax',string='Base Tax Calc', domain="[('type_tax_use','=','sale')]")
    #bank_tax_ids = fields.Many2many('account.tax',string='Bank Taxs')
	
    '''
    bank_commission_ids = fields.One2many(
		comodel_name='account.journal.bank.commission',
		inverse_name='journal_bank_id',
		string='Comisiones',
	)
    '''