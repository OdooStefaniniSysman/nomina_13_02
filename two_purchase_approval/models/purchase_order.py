from odoo import models,api,fields

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    state =  fields.Selection(selection_add=[('deparment', 'WAITING DEPARMENT APPROVAL'),('waiting','WAITING IR APPROVAL'),('done','DONE')])

    def validation_mount_department(self):
        self.state = 'deparment'
        res = self.notification_department()
        return res
    
    def validation_mount_waiting(self):
        if self.amount_total >= 8000000:
            self.state = 'waiting'
            res = self.notification_waiting()
        else:
            res = super(PurchaseOrder,self).button_approve()
        return res
   
    def notification_department(self):
        imd = self.env['ir.model.data']
        for record in self:
            partners = record.message_follower_ids.partner_id.ids
            users = self.env['res.users'].search([('partner_id.id', 'in', partners)])
            ids = []
            for user in users:
                ids.append((4, user.id))
        vals_wiz = {
            'message': 'Purchase order '+record.name+' in state '+record.state+' please,check',
            'users_ids': ids,
        }
        wiz_id = self.env['wizard.purchase'].create(vals_wiz)
        action = imd.xmlid_to_object('two_purchase_approval.action_create_wizard_deparment')
        form_view_id = imd.xmlid_to_res_id('two_purchase_approval.view_wizard_deparment')
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

    def notification_waiting(self):
        imd = self.env['ir.model.data']
        for record in self:
            partners = record.message_follower_ids.partner_id.ids
            users = self.env['res.users'].search([('partner_id.id', 'in', partners)])
            ids = []
            for user in users:
                ids.append((4, user.id))
        vals_wiz = {
            'message': 'Purchase order '+record.name+' in state '+record.state+' please,check',
            'users_ids': ids,
        }
        wiz_id = self.env['wizard.purchase'].create(vals_wiz)
        action = imd.xmlid_to_object('two_purchase_approval.action_create_wizard_waiting')
        form_view_id = imd.xmlid_to_res_id('two_purchase_approval.view_wizard_waiting')
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