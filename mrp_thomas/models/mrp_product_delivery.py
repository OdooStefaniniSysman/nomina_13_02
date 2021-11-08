#Luis Felipe Paternina
#Ingeniero de Sistemas
#Todoo SAS
from odoo import models, fields, api

class MrpProductDelivery(models.Model):
    _name = 'mrp.product.delivery'
    _description = 'Entrega de Productos'

    name = fields.Char(string="Nombre")
    address = fields.Char(string="Dirección")
    quantity = fields.Integer(string="Cantidad")