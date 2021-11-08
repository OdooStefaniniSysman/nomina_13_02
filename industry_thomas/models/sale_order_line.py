#Luis Felipe Paternina
#Ingeniero de Sistemas
#Todoo SAS
from odoo import models, fields, api

class Todoo(models.Model):
    _inherit = 'sale.order.line'

    time_of_so = fields.Char(string="Tiempo de Entrega")
    
     
    