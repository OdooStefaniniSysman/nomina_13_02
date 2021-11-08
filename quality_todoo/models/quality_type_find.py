from odoo import models, fields, api

class QualityTypeFind(models.Model):
    _name = 'quality.type.find'
    _description = "Tipos de hallazgo"

    name = fields.Char(string="Nombre", tracking=True)