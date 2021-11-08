# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class MrpWorkcenterProductivityLoss(models.Model):
    _inherit = 'mrp.workcenter.productivity.loss'
    
    code_tracking = fields.Integer('Tracking Code')
    