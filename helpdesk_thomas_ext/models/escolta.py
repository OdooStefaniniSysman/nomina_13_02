# -*- coding: utf-8 -*-

from odoo import models, fields, api

class HelpdeskEscolta(models.Model):
    _name = 'helpdesk.escolta'

    name = fields.Char(string="Nombre")