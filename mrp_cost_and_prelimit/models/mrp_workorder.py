   # -*- coding: utf-8 -*-

from odoo import models, fields, api


class MrpWorkorder(models.Model):
    _inherit = 'mrp.workorder'
   
    estimated_time = fields.Float('Tiempo estimado', default = 0.0)