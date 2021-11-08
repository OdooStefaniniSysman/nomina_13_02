# -*- coding: utf-8 -*-

from odoo import api, fields, models

class ResCompanyConsortium(models.Model):
    _name = 'res.consortium.members'
    _description = 'Consortium member companies'

    consortium_id = fields.Many2one('res.company', string='Consortium or Temporary union')
    partner_id = fields.Many2one('res.partner', string='Company')
    percent_part = fields.Float(string='% Participation', digits=(4,2))
    note1 = fields.Text(string='Note 1')
    note2 = fields.Text(string='Note 2')
    note3 = fields.Text(string='Note 3')
    
    
    
