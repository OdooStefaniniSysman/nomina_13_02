from odoo import models, fields, api

class HelpdeskUsers(models.Model):
    _inherit = 'res.users'

    group_users_id = fields.Many2one('helpdesk.groupusers', string="Group Users")