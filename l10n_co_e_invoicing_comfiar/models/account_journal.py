# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

class AccountJournal(models.Model):
    _inherit = 'account.journal'

    # is_einvoicing = fields.Boolean(string='electronic invoicing?')
    resolution_text = fields.Text(string='Resolución')
    sale_journal_type = fields.Selection([
        ('no', 'N/A'), 
        ('einv', 'E-invoicing'),
        ('reco', 'Recognition journal')],string='Sale Journal Type', default='no')
    account_recognition_id = fields.Many2one('account.account', string='Account recognition')
    
    
    
