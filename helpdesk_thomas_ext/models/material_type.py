# -*- coding: utf-8 -*-

from odoo import models, fields, api

class HelpdeskMaterialType(models.Model):
    _name = 'helpdesk.material.type'

    name = fields.Char(string="Type Material")
