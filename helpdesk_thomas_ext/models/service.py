# -*- coding: utf-8 -*-

from odoo import models, fields, api

class HelpdeskService(models.Model):
    _name = 'helpdesk.service'

    name = fields.Char(string= 'Nombre')
    team_id = fields.Many2one('helpdesk.team', string='Equipo')
    subservice_ids = fields.One2many('helpdesk.subservice','service_id',string='Subservicios')
    group_users_id = fields.Many2many('helpdesk.groupusers', string="Group Users")
    ticket_type = fields.Selection([('incidents', 'Incidente'),('request','Solicitud')], string='Ticket type')
    group_users_id = fields.Many2many('helpdesk.groupusers', string="Group Users")
    user_id = fields.Many2one('res.users', string="Usuario asignado")
