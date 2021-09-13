# -*- coding: utf-8 -*-

from odoo import models, fields, api

class HelpdeskProducto(models.Model):
    _name = 'helpdesk.personas'

    name = fields.Char(string= 'Nombre')
    cedula = fields.Integer(string= 'Cédula')
    serial_equipo = fields.Char(string= 'Serial equipo')
    empresa = fields.Char(string= 'Empresa')
    arl = fields.Char(string= 'Arl')
    eps = fields.Char(string= 'Eps')
    fecha_arl = fields.Date(string= 'Fecha de validez Arl')
    personas_ids = fields.Many2one('helpdesk.ticket', invisible=1)