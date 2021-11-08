
from odoo import models, fields, api

class MrpAdverse(models.Model):
    _name = 'mrp.adverse'
    _description = 'Descripción Anverso'

    name = fields.Char(string="Nombre")
    