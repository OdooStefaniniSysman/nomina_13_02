#Luis Felipe Paternina
#Ingeniero de Sistemas
#Todoo SAS
from odoo import models, fields, api

class MrpCosts(models.Model):
    _name = 'mrp.costs'
    _description = 'Costos de Producción'

    name = fields.Char(string="Nombre")
    total_cost = fields.Char(string="Costo Total")