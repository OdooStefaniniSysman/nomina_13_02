#Luis Felipe Paternina
from odoo import models, fields, api

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    sap_code = fields.Char(string="Código SAP")