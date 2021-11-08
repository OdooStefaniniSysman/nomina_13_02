# -*- coding: utf-8 -*-
from odoo import models,fields,api,_
import logging

_logger = logging.getLogger(__name__)

class MrpWorkorder(models.Model):
    _inherit = 'mrp.workorder'

    prelimit_code = fields.Char(related='workcenter_id.code')
    hours = fields.Float('Hours')
    distribution = fields.Float(compute='_compute_distribution')
    distribution_percentage = fields.Float('% Distribution',compute='_compute_distribution_percentage')
    
    @api.depends('hours')
    def _compute_distribution(self):
        for record in self:
            record.distribution = sum( record.env['mrp.workorder'].search([('workcenter_id','=',record.workcenter_id.id)]).mapped('hours'))
            """"if record.workcenter_id.id == 1:
               total_hour += record.hours
               record.distribution = total_hour
            elif record.workcenter_id.id == 2:
               total_hour2 += record.hours
               record.distribution = total_hour2
            else:
                self.distribution = 0"""
    
    @api.depends('workcenter_id')
    def _compute_distribution_percentage(self):
        for record in self:
            if record.workcenter_id.id == 1 and record.distribution != 0:
                record.distribution_percentage = record.hours/record.distribution
            elif record.workcenter_id.id == 2 and record.distribution != 0:
                record.distribution_percentage = record.hours/record.distribution
            else:
                record.distribution_percentage = 0