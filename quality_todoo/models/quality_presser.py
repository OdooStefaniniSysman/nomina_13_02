#Todoo SAS

from odoo import models, fields, api

class QualityCheck(models.Model):
    _name = 'quality.presser'

    name = fields.Char(string="Nombre")
    cc = fields.Char(string="Cédula")