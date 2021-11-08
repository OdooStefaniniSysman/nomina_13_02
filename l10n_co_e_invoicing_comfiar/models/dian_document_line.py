# -*- coding: utf-8 -*-

from odoo import models, fields, _
from odoo.exceptions import ValidationError, UserError

class DianDocumentLine(models.Model):
    _name = "dian.document.line"

    dian_document_id = fields.Many2one('account.invoice.dian.document', string='DIAN Document')
    invoice_id = fields.Many2one('account.move', string='Invoice')
    partner_id = fields.Many2one('res.partner', string='Customer')    
    start_state = fields.Selection([('0', '0'), 
                                   ('1', '1'),
                                   ('2', '2'),
                                   ('3', '3'),
                                   ('10', '10'),
                                   ('11', '11'),
                                   ('12', '12')], string='Start State')
    end_state = fields.Selection([('0', '0'), 
                                   ('1', '1'),
                                   ('2', '2'),
                                   ('3', '3'),
                                   ('10', '10'),
                                   ('11', '11'),
                                   ('12', '12')], string='End State')
    state_comfiar = fields.Char(string='Status Comfiar')
    description = fields.Char(string='Description')
    
    
    
    