# -*- coding: utf-8 -*-

from odoo import models, fields, api

class HelpdeskProducto(models.Model):
    _name = 'helpdesk.producto'

    name = fields.Char(string= 'Nombre')
    unidad = fields.Char(string= 'Unidad de medida')
    cantidad = fields.Integer(string= 'Cantidad')
    producto_ids = fields.Many2one('helpdesk.ticket', invisible=1)