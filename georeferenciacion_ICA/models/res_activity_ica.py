# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResActivityIca(models.Model):
    _name = 'res.activity.ica'
    _description = 'Actividades relacionadas con los impuestos ICA'

    name = fields.Char(string='Actividad')
