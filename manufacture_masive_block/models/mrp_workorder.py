# -*- coding: utf-8 -*-

from odoo import _, api, fields, models


class MrpWorkorder(models.Model):
    _inherit = 'mrp.workorder'
    
    bool_state = fields.Boolean(compute="_compute_bool_state")
    
    @api.depends('production_id')
    def _compute_bool_state(self):
        if self.production_id.bool_state:
            self.bool_state = True
        else:
            self.bool_state = False