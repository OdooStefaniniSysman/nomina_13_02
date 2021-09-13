# -*- coding: utf-8 -*-

from odoo import models, fields, api

class HelpdeskTypeTicket(models.Model):
    _name = 'helpdesk.type'

    name = fields.Char(string="Tipo de Ticket")