# -*- coding: utf-8 -*-
from odoo import models,fields,api,_
import logging

_logger = logging.getLogger(__name__)

class MrpPrelimit(models.Model):
    _name = 'mrp.prelimit'
    _description = 'mrp prelimit'
    _rec_name = 'workcenter_id'

    prelimit_code = fields.Char(related='workcenter_id.code')
    workcenter_id = fields.Many2one('mrp.workcenter','Workcenter')
    date_start = fields.Date()
    date_end = fields.Date()
    production_id = fields.Many2one('mrp.production','Production Order')
    hours = fields.Float('Hours')
    distribution = fields.Float(compute='_compute_distribution')
    distribution_percentage = fields.Float('% Distribution',compute='_compute_distribution_percentage')
    cost_mod = fields.Float(compute='_compute_cost_mod')
    cost_cif = fields.Float(compute='_compute_cost_cif')
    cost_maq = fields.Float(compute='_compute_cost_maq')
    
    
    @api.depends('workcenter_id')
    def _compute_cost_maq(self):
        for record in self:
            if record.workcenter_id:
                account_id_maq = sum(record.env['account.move.line'].search([('account_id','=',record.workcenter_id.maq_account_id_real.id),('date','>=',record.date_start),('date','<=',record.date_end)]).mapped('debit'))
                record.cost_maq = record.distribution_percentage * account_id_maq
            else:
                record.cost_maq = 0
                
    
    @api.depends('workcenter_id')
    def _compute_cost_cif(self):
        for record in self:
            if record.workcenter_id:
                account_id_cif = sum(record.env['account.move.line'].search([('account_id','=',record.workcenter_id.cif_account_id_real.id),('date','>=',record.date_start),('date','<=',record.date_end)]).mapped('debit'))
                record.cost_cif = record.distribution_percentage * account_id_cif
            else:
                record.cost_cif = 0
                
            
    @api.depends('workcenter_id')
    def _compute_cost_mod(self):
        for record in self:
            if record.workcenter_id:
                account_id_mod = sum(record.env['account.move.line'].search([('account_id','=',record.workcenter_id.mod_account_id_real.id),('date','>=',record.date_start),('date','<=',record.date_end)]).mapped('debit'))
                record.cost_mod = record.distribution_percentage * account_id_mod
            else:
                record.cost_mod = 0
                
    
    @api.depends('hours')
    def _compute_distribution(self):
        for record in self:
            record.distribution = sum( record.env['mrp.prelimit'].search([('workcenter_id','=',record.workcenter_id.id)]).mapped('hours'))
            #record.distribution = sum(record.env['mrp.prelimit'].browse([record.workcenter_id.id].mapped('hours')))
    
    @api.depends('workcenter_id')
    def _compute_distribution_percentage(self):
        for record in self:
            if record.workcenter_id.id == 1 and record.distribution != 0:
                record.distribution_percentage = record.hours/record.distribution
            elif record.workcenter_id.id == 2 and record.distribution != 0:
                record.distribution_percentage = record.hours/record.distribution
            else:
                record.distribution_percentage = 0