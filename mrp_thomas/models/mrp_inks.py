#Luis Felipe Paternina
#Ingeniero de Sistemas
#Todoo SAS
from odoo import models, fields, api

class MrpInksThomas(models.Model):
    _name = 'mrp.inks'
    _description = 'Tintas para cada componente o Documento'

    name = fields.Char(string="Nombre")
    inks_category = fields.Selection([('plana','Plana'),('continua','Continua')], string="Tintas para cada componente o Documento")