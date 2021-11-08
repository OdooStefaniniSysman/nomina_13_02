from odoo import fields,models,api

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    maintenance_id = fields.Many2one('maintenance.request')