# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResActivityCityIca(models.Model):
    _name = 'res.activity.city.ica'
    _description = 'Actividades relacionadas con los impuestos ICA asociando la ciudad por tercero'

    name = fields.Char(string='name')
    city_id = fields.Many2one('res.city.zip', string='Ciudad')
    activity_ids = fields.Many2many('res.activity.ica', string='Actividades')
    partner_id = fields.Many2one('res.partner', string='Tercero')
