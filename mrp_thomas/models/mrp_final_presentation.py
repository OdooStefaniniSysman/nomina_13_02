#Luis Felipe Paternina
#Ingeniero de Sistemas
#Todoo SAS
from odoo import models, fields, api

class MrpFinalPresentation(models.Model):
    _name = 'mrp.final.presentation'
    _description = 'Presentación Final'

    name = fields.Char(string="Nombre")
    