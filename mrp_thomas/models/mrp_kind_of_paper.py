#Luis Felipe Paternina
#Ingeniero de Sistemas
#Todoo SAS
from odoo import models, fields, api

class MrpKindPaper(models.Model):
    _name = 'mrp.kind.paper'
    _description = 'Tipo de papel Thomas Producción'

    name = fields.Char(string="Tipo de Papel")
    paper_category = fields.Selection([('plana','Planas'),('continua','Continua')])
    grammage = fields.Char(string="Gramaje")