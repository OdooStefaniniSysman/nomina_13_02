# -*- coding: utf-8 -*-

from odoo import models, fields, api

class HelpdeskProductoMuestras(models.Model):
    _name = 'helpdesk.producto.muestras'

    name = fields.Char(string= 'Nombre')
    cliente = fields.Char(string= 'Cliente')
    cantidad = fields.Integer(string= 'Cantidad')
    sett = fields.Integer(string= 'SET')
    orden_produccion = fields.Char(string= 'Orden de producción')
    producto_muestras_ids = fields.Many2one('helpdesk.ticket', invisible=1)