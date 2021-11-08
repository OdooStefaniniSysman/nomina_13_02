# -*- coding: utf-8 -*-

from odoo import models, fields, api

class HelpdeskSubService(models.Model):
    _name = 'helpdesk.subservice'

    name = fields.Char(string="Nombre subservicio")
    service_id = fields.Many2one('helpdesk.service', string="Servicio relacionado")
    group_users_id = fields.Many2many('helpdesk.groupusers', string="Group Users")
    team_id = fields.Many2one('helpdesk.team', string="Mesa de ayuda relacionado")
