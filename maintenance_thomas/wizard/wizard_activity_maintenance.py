from odoo import api, fields, models


class ActivityWizardMaintenance(models.TransientModel):
    _name = "wizard.maintenance"
    _description = 'wizard create maintenance'

    message = fields.Text('observations')
    users_ids = fields.Many2many('res.users', 'users_maintenance_rel', 'maintenance_id', 'user_id', 'Users')

    def action_create_activity(self):
        for record in self:
            maintenance_id = self.env['maintenance.request'].browse(self._context.get('active_id'))
            model_id = self.env.ref('maintenance_thomas.model_maintenance_request')
            type_id = self.env.ref('mail.mail_activity_data_todo')
            summary = record.message
            users = record.users_ids
            for user in users:
                activity_data = {
                    'res_id': maintenance_id.id,
                    'res_model_id': model_id.id,
                    'activity_type_id': type_id.id,
                    'summary': summary,
                    'user_id': user.id,
                }
                self.env['mail.activity'].sudo().create(activity_data)