#Luis Felipe Paternina
#Ingeniero de Sistemas
#Todoo SAS

from odoo import models, fields, api

class ResCompany_tst(models.Model):
    _inherit = 'res.company'

    img_incontec = fields.Binary(string="Logo Incontec")
    logo_tst = fields.Binary(string="Logo de la Compañía")
    