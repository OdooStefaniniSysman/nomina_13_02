# -*- coding: utf-8 -*-

from odoo import models, fields, api

class HelpdeskAns(models.Model):
    _inherit = 'helpdesk.sla'

    activity_id = fields.Many2one('helpdesk.activity', 'Actividad')
