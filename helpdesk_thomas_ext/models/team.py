# -*- coding: utf-8 -*-

from odoo import models, fields, api

class HelpdeskTeam(models.Model):
    _inherit = 'helpdesk.team'

    team_id = fields.Many2one('helpdesk.team', string='Team Helpdesk')

    helpdesk_team = fields.Selection([('selection_1', 'selection 1'),
                                      ('selection_2', 'selection 2')], string='Typology helpdesk')

    helpdesk_team_tipology = fields.Char(compute='_get_label_team', string='Helpdesk Tipology')


    @api.depends('helpdesk_team')
    def _get_label_team(self):
        for record in self:
            if record.helpdesk_team == 'selection_1':
                record.helpdesk_team_tipology = 'Selection 1'
            if record.helpdesk_team == 'selection_2':
                record.helpdesk_team_tipology = 'Selection 2'
            if record.helpdesk_team == False:
                record.helpdesk_team_tipology = False
