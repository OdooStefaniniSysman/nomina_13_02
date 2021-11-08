#Luis Felipe Paternina
#Ingeniero de Sistemas
#Todoo SAS
from odoo import models, fields, api

class MrpPackingForm(models.Model):
    _name = 'mrp.packing.form'
    _description = 'Forma de Empaque'

    name = fields.Char(string="Nombre")
    