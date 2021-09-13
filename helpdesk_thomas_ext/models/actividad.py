# -*- coding: utf-8 -*-

from odoo import models, fields, api

class HelpdeskTypeActivity(models.Model):
    _name = 'helpdesk.activity'

    name = fields.Char(string="Nombre Actividad")
    service_id = fields.Many2one('helpdesk.service', string="Servicio relazionado")
    subservice_id = fields.Many2one('helpdesk.subservice', string="Subservicio")
    users_id = fields.Many2one('res.users', string="Usuario")
    users_ids = fields.Many2many('res.users', string="Usuarios a relacionar")
    helpdesk_ticket_id = fields.Many2one('helpdesk.ticket')
    #type_ticket_id = fields.Many2one('helpdesk.type', string="Ticket type")
    ticket_type = fields.Selection([('incidents', 'Incidentes'),('request','Solicitud')], string='Ticket type')
    team_id = fields.Many2one('helpdesk.team', string='Mesa de ayuda relaciadona')
    file_request = fields.Boolean(string="File Request")
    group_users_id = fields.Many2one('helpdesk.groupusers', string="Group Users")
    user_group_activity = fields.Selection([('infrastrucutre', 'Infraestructura'),
                                      ('development', 'Desarrollo'),
                                      ('admin', 'Admin')], string="Sub Service")
    info_security = fields.Selection([('Si', 'Si'),
                                      ('No', 'No'),], string="Sub Service")
    
    priority = fields.Selection([('0', 'Baja'),
                                 ('1', 'Baja'),
                                ('2', 'Media'),
                                ('3', 'Alta')], string="Prioridad")

    asn_date = fields.Boolean(string="ASN Date")
    asn_high = fields.Integer(string="High")
    asn_medium = fields.Integer(string="Medium")
    asn_low = fields.Integer(string="Low")

