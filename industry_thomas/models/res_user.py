#Luis Felipe Paternina
from odoo import models, fields, api

class ResusersTst(models.Model):
    _inherit = 'res.users'

    is_technical = fields.Boolean(string="Técnico")
    technical_code = fields.Char(string="Código del Técnico")