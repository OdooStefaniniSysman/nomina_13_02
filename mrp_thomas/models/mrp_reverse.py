#Luis Felipe Paternina
#Ingeniero de Sistemas
#Todoo SAS
from odoo import models, fields, api

class MrpReverse(models.Model):
    _name = 'mrp.reverse'
    _description = 'Descripción Reverso'

    name = fields.Char(string="Nombre")