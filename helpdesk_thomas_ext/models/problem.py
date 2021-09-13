from odoo import models, fields, api

class HelpdeskProblem(models.Model):
    _name = 'helpdesk.problem'

    name = fields.Char(string="Name")

