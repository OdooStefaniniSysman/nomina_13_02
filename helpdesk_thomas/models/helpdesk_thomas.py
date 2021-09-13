# -*- coding: utf-8 -*-

from odoo import models, fields, api

class HelpdeskTicket(models.Model):
    _inherit = 'helpdesk.ticket'

    val_req_contact = fields.Boolean(string="Valid requirements")
    tiket_number_contract = fields.Char(string='Ticket number Legal management')
    maintenance_equipment_id = fields.Many2one(
        'maintenance.equipment',
        string='Maintenance Equipment',
        )
    equipment_model = fields.Char(string='Model')
    equipment_serial = fields.Char(string='Brand')
    # equipment_customer = fields.Char(string='Equipment related customer')
    equipment_supplier = fields.Char(string='Supplier associated to the guarantee')
    guarantee_reply = fields.Char(string='Guarantee reply')
    inventory_ubication = fields.Selection([('product in cellar', 'product in cellar'),('product at supplier location','product at supplier location')], string='Inventory ubication')
    customer_response = fields.Char(string='Customer response')

    @api.onchange('maintenance_equipment_id')
    def onchange_maintenance_equipment_id(self):
        self.equipment_model = self.maintenance_equipment_id.model
        self.equipment_serial = self.maintenance_equipment_id.serial_no
        self.partner_id = self.maintenance_equipment_id.partner_client_id.id
        self.equipment_supplier =self.maintenance_equipment_id.partner_id.name
    