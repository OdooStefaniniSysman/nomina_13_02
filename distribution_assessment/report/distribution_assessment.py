# -*- coding: utf-8 -*-
import logging
from odoo import fields, models, tools, api,_
from datetime import datetime
from odoo.osv import expression
from odoo.tools import date_utils

_logger = logging.getLogger(__name__)

    
class DistributionAssessment(models.Model):
    _name = 'report.distribution.assessment'
    _auto = False
    _description = 'This is the lines in the Distribution Assessment report'
    
    name = fields.Char('Workcenter',readonly=True)
    date_end = fields.Datetime('Date',readonly=True)
    hours = fields.Float('Hours',readonly=True)
    total_time = fields.Float('Total Times',readonly=True)
    percentage = fields.Float('%',readonly=True)
    management = fields.Float('Operation Management',readonly=True)
    laboratory = fields.Float('Laboratory',readonly=True)
    dispatch = fields.Float('Dispatch',readonly=True)
    maintenance = fields.Float('Maintenance',readonly=True)
    disused_assets = fields.Float('Disused Assets',readonly=True)
    alternative_center = fields.Float('Alternative Center',readonly=True)
    code = fields.Char('Code',readonly=True)
    
    def init(self):
        tools.drop_view_if_exists(self._cr, 'report_distribution_assessment')
        query = """
            CREATE or REPLACE VIEW report_distribution_assessment AS(
            select 
            row_number() OVER (ORDER BY w.id)as id,
            w.name,sum(mwp.duration) as hours,mwp.date_end,
            (
             select sum(mwp.duration) 
             from mrp_workcenter_productivity mwp
            ) as total_time,
            (
             sum(mwp.duration)/(select sum(mwp.duration) 
             from mrp_workcenter_productivity mwp)
            )as percentage,
            (
             (
             select sum(aml.debit) 
             from account_move_line aml
             left join account_analytic_account aaa on (aaa.id = aml.analytic_account_id)
             where aml.analytic_account_id = 3436
             )
             *
             (
             sum(mwp.duration)/(select sum(mwp.duration) 
             from mrp_workcenter_productivity mwp)
             )
            )as management,
            (
             (
             select sum(aml.debit) 
             from account_move_line aml
             left join account_analytic_account aaa on (aaa.id = aml.analytic_account_id)
             where aml.analytic_account_id = 3437
             )
             *
             (
             sum(mwp.duration)/(select sum(mwp.duration) 
             from mrp_workcenter_productivity mwp)
             )
            )as laboratory,
            (
             (
             select sum(aml.debit) 
             from account_move_line aml
             left join account_analytic_account aaa on (aaa.id = aml.analytic_account_id)
             where aml.analytic_account_id = 3438
             )
             *
             (
             sum(mwp.duration)/(select sum(mwp.duration) 
             from mrp_workcenter_productivity mwp)
             )
            )as dispatch,
            (
             (
             select sum(aml.debit) 
             from account_move_line aml
             left join account_analytic_account aaa on (aaa.id = aml.analytic_account_id)
             where aml.analytic_account_id = 3439
             )
             *
             (
             sum(mwp.duration)/(select sum(mwp.duration) 
             from mrp_workcenter_productivity mwp)
             )
            )as maintenance,
            (
             (
             select sum(aml.debit) 
             from account_move_line aml
             left join account_analytic_account aaa on (aaa.id = aml.analytic_account_id)
             where aml.analytic_account_id = 3441
             )
             *
             (
             sum(mwp.duration)/(select sum(mwp.duration) 
             from mrp_workcenter_productivity mwp)
             )
            )as disused_assets,
            (
             (
             select sum(aml.debit) 
             from account_move_line aml
             left join account_analytic_account aaa on (aaa.id = aml.analytic_account_id)
             where aml.analytic_account_id = 3442
             )
             *
             (
             sum(mwp.duration)/(select sum(mwp.duration) 
             from mrp_workcenter_productivity mwp)
             )
            )as Alternative_center,
            (
             --select aaa.code 
             --from account_analytic_account aaa
             --left join mrp_workcenter w on (w.account_analytic_real = aaa.id)
             --left join mrp_workcenter_productivity mwp on (mwp.workcenter_id = w.id)
             --where mwp.workcenter_id = w.id
             --group by w.id, w.name, aaa.code
            aaa.code ) as code
            from mrp_workcenter_productivity mwp
            left join mrp_workcenter w on (w.id = mwp.workcenter_id)
            left join account_analytic_account aaa on (aaa.id = w.account_analytic_real)
            where 1=1
            group by w.id, w.name, aaa.code, mwp.date_end
            );
            """
        self.env.cr.execute(query)
    
#class MrpCostStructureSupra(models.AbstractModel):
 #   _name = 'report.distribution_assessment.distribution_assessment_structure'
  #  _description = 'MRP Distribution Assessment'

   # def get_lines(self, workorders):
    #    res = []
     #   workorder = []
      #  total_hours = []
       # query_str = """select row_number() OVER (ORDER BY w.id)as id,
        #                w.name as name,sum(mwp.duration) as hours,sum(mwp.)
        #                from mrp_workcenter_productivity mwp
        #                left join mrp_workcenter w on (w.id = mwp.workcenter_id)
        #                in %s 
        #                group by w.id, w.name"""
        #self.env.cr.execute(query_str, (tuple(workorders.ids), ))
        #for name, hours in self.env.cr.fetchall():
        #    workorder.append([name,hours])
        #    for hour in workorders.duration:
        #        total_hour += hour
        #        total_hours.append([total_hour])
        #    res.append({
        #        'workorder':workorder,
        #        'total_hours':total_hours,
        #    })
        #return res
        
    #@api.model
    #def _get_report_values(self):
    #    workorders = self.env['mrp.workorder']
    #        res = self.get_lines(workorders)
    #    return {'lines': res}