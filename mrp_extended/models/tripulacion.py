from odoo import models,fields,api
import logging
from itertools import chain
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError



logger = logging.getLogger(__name__)


class WorkOrderTripulacion(models.Model):
    _inherit = 'mrp.workorder'
    _description = 'Work Order'
    operators_test = fields.Float('Number of Operators TEST', compute='_compute_real_time_operator', store=True)
    operators = fields.Float('Number of Operators')
    #,  compute='_compute_real_time_operator', store=True
    real_time_operator = fields.Float('Tiempo real operador', compute='_compute_real_time_operator', store=True)
    real_time_operator_line = fields.Float(' Real Tiempo real operador')
    
    @api.depends('time_ids.real_time_operator_line')
    def _compute_real_time_operator(self):
        for order in self:
            order.real_time_operator = sum(order.time_ids.mapped('real_time_operator_line'))
            #order.operators = sum(order.time_ids.mapped('operators_number'))
            
    
    def check_number_operators(self):
        if self.operators == 0:
            raise ValidationError((
                'Error ! El número de operarios no puede ser 0.'))
        return
    
    def _get_duration_total_tripulation(self):
        self.duration
        return
    
   
    
    
    
    #def write(self, values):
               #super(MrpWorkorder, self).write(values)     
        #return super(MrpWorkorder, self).write(values)
    
    def button_pending(self):
        #self.check_number_operators()
        self.end_previous()
        #self.check_number_operators() 
        #self. _compute_real_time_operator()
        #qui = self._mrp_workcenter_productivity_object()
        #qui._get_operators_number_workorder()
        qui = self.env['mrp.workcenter.productivity'].search([('workorder_id', '=', self.id)])
        a = qui[0]
        logger.info('**************7*********')
        #a._compute_duration()
        logger.info(a.duration)
        logger.info(self.duration)
        operators_test = self.duration * 2
        logger.info(self.operators_test)
        #self.check_number_operators
        if self.operators != 0.0:
            a.operators_number = self.operators
            a.real_time_operator_line = a.operators_number * a.duration 
        self.check_number_operators()
        #self._get_duration_total_tripulation()
        return True
    
    def do_finish(self):
        self.record_production()
        self.check_number_operators() 
        # workorder tree view action should redirect to the same view instead of workorder kanban view when WO mark as done.
        if self.env.context.get('active_model') == self._name:
            action = self.env.ref('mrp.action_mrp_workorder_production_specific').read()[0]
            action['context'] = {'search_default_production_id': self.production_id.id}
            action['target'] = 'main'
        else:
            # workorder tablet view action should redirect to the same tablet view with same workcenter when WO mark as done.
            action = self.env.ref('mrp_workorder.mrp_workorder_action_tablet').read()[0]
            action['context'] = {
                'form_view_initial_mode': 'edit',
                'no_breadcrumbs': True,
                'search_default_workcenter_id': self.workcenter_id.id
            }
        action['domain'] = [('state', 'not in', ['done', 'cancel', 'pending'])]
        qui = self.env['mrp.workcenter.productivity'].search([('workorder_id', '=', self.id)])
        a = qui[0]
        logger.info('**************7*********')
        #a._compute_duration()
        logger.info(a.duration)
        logger.info(self.duration)
        operators_test = self.duration * 2
        logger.info(self.operators_test)
        self.check_number_operators
        if self.operators != 0.0:
            a.operators_number = self.operators
            a.real_time_operator_line = a.operators_number * a.duration 
        ####
        #self.check_number_operators() 
        return action
    

    
    def button_done(self):
        qui = self.env['mrp.workcenter.productivity'].search([('workorder_id', '=', self.id)])
        a = qui[0]
        logger.info('**************7*********')
        #a._compute_duration()
        logger.info(a.duration)
        logger.info(self.duration)
        operators_test = self.duration * 2
        logger.info(self.operators_test)
        self.check_number_operators
        if self.operators != 0.0:
            a.operators_number = self.operators
            a.real_time_operator_line = a.operators_number * a.duration 
        self.check_number_operators()
        #self._get_duration_total_tripulation()
        if any([x.state in ('done', 'cancel') for x in self]):
            raise UserError(_('A Manufacturing Order is already done or cancelled.'))
        self.end_all()
        end_date = datetime.now()
        return self.write({
            'state': 'done',
            'date_finished': end_date,
            'date_planned_finished': end_date,
        })
        
    
class WorkOrderTripulacionProductivity(models.Model):
    _inherit = 'mrp.workcenter.productivity'

    operators = fields.Float('Number of Operators')
    operators_time = fields.Float('Tiemp real operarios')
    operators_number = fields.Float('Numero de operarios ')
    real_time_operator_line = fields.Float('Tiempo real operador',compute='_compute_real_time_operator_line')
    
    @api.depends('duration','operators_number')
    def _compute_real_time_operator_line(self):
        #self._check_operators_in_form()
        for record in self:
            if record.duration != 0.0 and record.operators_number != 0.0:
                record.real_time_operator_line = record.duration * record.operators_number
            else:
                record.real_time_operator_line = 0.0 

