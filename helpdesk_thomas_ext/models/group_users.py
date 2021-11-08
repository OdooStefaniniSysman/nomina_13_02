# -*- coding: utf-8 -*-

from odoo import models, fields, api

class HelpdeskGroupUsers(models.Model):
    _name = 'helpdesk.groupusers'

    name = fields.Char(string="Nombre del grupo")
    user_id = fields.Many2many('res.users', string="Usuarios")