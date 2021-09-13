# -*- coding: utf-8 -*-
from odoo import _, api, fields, models


class MrpProduction(models.Model):
    _inherit = 'mrp.production'
    
    state_block = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('planned', 'Planned'),
        ('progress', 'In Progress'),
        ('to_close', 'To Close'),
        ('done', 'Done'),
        ('cancel', 'Cancelled'),
        ('block', 'Block')])
        
    bool_state = fields.Boolean()
    
    def blocked(self):
        for record in self:
            record.state_block = 'block'
            record.bool_state = True
            
    def unblocked(self):
        for record in self:
            record.bool_state = False