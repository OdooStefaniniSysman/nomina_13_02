# -*- coding: utf-8 -*-

import logging
from odoo import fields, models, api, _
from odoo.tools import float_compare
from datetime import datetime
from odoo.exceptions import ValidationError, UserError


_logger = logging.getLogger(__name__)

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    session_id = fields.Many2one(
        'treasury.session', 
        string='Sesión', 
        required=False, 
        index=True,
        domain="[('state', '=', 'opened')]",
        readonly=True,
        store=True)
    config_id = fields.Many2one('treasury.config', related='session_id.config_id', string="C", readonly=False)
    
    @api.model
    def default_get(self, fields):
        vals = super(SaleOrder, self).default_get(fields)
        team_ids = self.env['crm.team'].search([('member_ids', '=', self.env.uid)])
        for team in team_ids:
            config_obj = self.env['treasury.config'].search([('crm_team_id', '=', team.id)], limit=1)
            session_obj = self.env['treasury.session'].search([('config_id', '=', config_obj.id),('state','=','opened')], limit=1)
            if session_obj.id:
                vals['session_id'] = session_obj.id
                return vals
        return vals
    

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4
