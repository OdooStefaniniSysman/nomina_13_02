# -*- coding: utf-8 -*-
from odoo import models, fields, api

class HelpdeskVigilante(models.Model):
    _name = 'helpdesk.vigilante'

    name = fields.Text(string="Nombre")