#Luis Felipe Paternina
#Ingeniero de Sistemas
#Todoo SAS
from odoo import models, fields, api

class MrpDocumentSize(models.Model):
    _name = 'mrp.document.size'
    _description = 'Tamaño de papel Thomas Producción'

    name = fields.Char(string="Tamaño del Documento")
    width = fields.Char(string="Ancho")
    heigth = fields.Char(string="Largo")
    