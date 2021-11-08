# -*- coding: utf-8 -*-

from odoo import models, fields, api

class HelpdeskServiceTeam(models.Model):
    _name = 'helpdesk.users'

    name = fields.Char('Usuarios asociados al grupo')