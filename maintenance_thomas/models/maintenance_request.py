from odoo import models,fields,api

class MaintenanceRequest(models.Model):
    _inherit = 'maintenance.request'

    metodology_control = fields.Selection([('calibration','Calibration'),('verification','Verification'),('maintenance','Maintenance')],'Metodology Control')
    variable = fields.Selection([('mass','Mass'),('dimension','Dimension'),('temperature','Temperature')],'Variable to size')
    unit_measure = fields.Many2one('uom.uom','Unit of Measure')
    range_measure = fields.Integer('Range Measure')
    tolerance = fields.Integer('Tolerance')
    mistake_equipment = fields.Char('Mistake Equipment')
    uncertainty_measure = fields.Char('Uncertainty Measure')
    fercuency = fields.Char('Frecuency')
    bool_quantity = fields.Boolean(compute='_compute_bool_quantity')
    maintenance_type = fields.Selection([('corrective','Corrective'),('preventive','Preventive'),('autonomous','Autonomous'),('pdae','PDAE')])
    employee_ids = fields.One2many('hr.employee','maintenance_id','Technicians')
    
    @api.depends('maintenance_team_id')
    def _compute_bool_quantity(self):
        if self.maintenance_team_id.name == 'CALIDAD':
            self.bool_quantity = True
        else:
            self.bool_quantity = False

    def action_create_wizard(self):
        imd = self.env['ir.model.data']
        for record in self:
            partners = record.message_follower_ids.partner_id.ids
            users = self.env['res.users'].search([('partner_id.id', 'in', partners)])
            ids = []
            for user in users:
                ids.append((4, user.id))
        vals_wiz = {
            'message': 'Petición de mantenimiento  '+record.name+'en '+record.stage_id.name ,
            'users_ids': ids,
        }
        wiz_id = self.env['wizard.maintenance'].create(vals_wiz)
        action = imd.xmlid_to_object('maintenance_thomas.action_create_maintenance')
        form_view_id = imd.xmlid_to_res_id('maintenance_thomas.view_message_activity')
        return {
            'name': action.name,
            'help': action.help,
            'type': action.type,
            'views': [(form_view_id, 'form')],
            'view_id': form_view_id,
            'target': action.target,
            'context': action.context,
            'res_model': action.res_model,
            'res_id': wiz_id.id,
        }

    def active_wizard(self):
        if self.stage_id.name == 'En progreso' or 'In Progress':
            self.action_create_wizard()
        return super(MaintenanceRequest,self).active_wizard()