from odoo import models, fields, api

class QualityProcess(models.Model):
    _name = 'quality.process'
    _description = "Procesos de Calidad"

    name = fields.Char(string="Nombre", tracking=True)