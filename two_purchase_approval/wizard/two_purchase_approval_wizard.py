from odoo import fields,models,api


class ActivityWizardPurchase(models.TransientModel):
    _name = "wizard.purchase"
    _description = 'wizard approval purchase'

    message = fields.Text('observations')
    users_ids = fields.Many2many('res.users', 'users_purchase_rel', 'purchase_id', 'user_id', 'Users')

    def action_wizard_deparment(self):
        for record in self:
            purchase_id = self.env['purchase.order'].browse(self._context.get('active_id'))
            model_id = self.env.ref('two_purchase_approval.model_purchase_order')
            type_id = self.env.ref('mail.mail_activity_data_todo')
            summary = record.message
            users = record.users_ids
            for user in users:
                activity_data = {
                    'res_id': purchase_id.id,
                    'res_model_id': model_id.id,
                    'activity_type_id': type_id.id,
                    'summary': summary,
                    'user_id': user.id,
                }
                self.env['mail.activity'].sudo().create(activity_data)

    def action_wizard_waiting(self):
        for record in self:
            purchase_id = self.env['purchase.order'].browse(self._context.get('active_id'))
            model_id = self.env.ref('two_purchase_approval.model_purchase_order')
            type_id = self.env.ref('mail.mail_activity_data_todo')
            summary = record.message
            users = record.users_ids
            for user in users:
                activity_data = {
                    'res_id': purchase_id.id,
                    'res_model_id': model_id.id,
                    'activity_type_id': type_id.id,
                    'summary': summary,
                    'user_id': user.id,
                }
                self.env['mail.activity'].sudo().create(activity_data)