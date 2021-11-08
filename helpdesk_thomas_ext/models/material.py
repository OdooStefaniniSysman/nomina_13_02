# -*- coding: utf-8 -*-

from odoo import models, fields, api

class HelpdeskMaterial(models.Model):
    _name = 'helpdesk.material'

    name = fields.Char(string= 'Nombre')
    cantidad = fields.Integer(string= 'Cantidad')
    unidad = fields.Char(string= 'Unidad de medida')
    cliente= fields.Char(string= 'Cliente')
    material_ids = fields.Many2one('helpdesk.ticket', invisible=1)
