# -*- coding: utf-8 -*-

from odoo import models, fields, api

class HelpdeskDepartament(models.Model):
    _inherit = 'res.users'

    departament = fields.Char(string="Departament")