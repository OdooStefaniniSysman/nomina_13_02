# -*- coding: utf-8 -*-

from odoo import fields, models

class ResUsers(models.Model):
    _inherit = 'res.users'

    treasury_config_ids = fields.Many2many('treasury.config', string='Cajas Menores Disponibles', help="Cajas Menores disponibles para el usuario cuando este último pertenece al rol: Usuario de Cajas Menores. El rol de administrador puede ver todas las cajas menores.")
