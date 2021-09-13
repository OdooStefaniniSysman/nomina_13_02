# -*- coding: utf-8 -*-


from odoo import models, fields, api, _


class MaintenanceEquipment(models.Model):
    _inherit = 'maintenance.equipment'

    partner_client_id = fields.Many2one('res.partner', string='Client')
    actual_location = fields.Char(string='Actual machine location')
    model = fields.Char(string='Model')
    # brand = fields.Char(string='Brand')
    


# class MaintenanceRequest(models.Model):
#     _inherit = 'maintenance.request'

#     service_order = fields.Char(string="Service Order", readonly = True, index=True, default=lambda self: _('New'))
#     partner_client_id = fields.Many2one('res.partner', string='Client')
#     client_city = fields.Char(string="City")
#     contract_code = fields.Char(string="Contract code")
#     contract_end = fields.Char(string="End date of the contract")
#     aprobation_type = fields.Char(string="Spare parts approval type")
#     equipment_serie = fields.Char(string="Equipment serie")
#     equipment_brand = fields.Char(string="Equipment brand")
#     equipment_model = fields.Char(string="Model")
#     maintenance_type = fields.Selection(selection_add=[('Instalacion de maquina','Instalacion de maquina'),
#                                         ('Alistamiento','Alistamiento'),
#                                         ('Instalacion de respuesto','Instalacion de repuesto')]) 
#     equipment_location = fields.Char(string="Current location")

#     @api.onchange('partner_client_id')
#     def _onchange_partner_client_id(self):
#         self.client_city = self.partner_client_id.city_crm.name
#         self.contract_code = self.partner_client_id.contract_number_tst
#         self.contract_end = str(self.partner_client_id.contract_end_date_tst)
#         self.aprobation_type = self.partner_client_id.aprobation_type_tst

#     @api.onchange('equipment_id')
#     def _onchange_equipment_id(self):
#         self.equipment_serie = self.equipment_id.serial_no
#         self.equipment_brand = self.equipment_id.brand
#         self.equipment_model = self.equipment_id.model
#         self.equipment_location = self.equipment_id.location


#     @api.model
#     def create(self, vals):
#         if vals.get('service_order', _('New')) == _('New'):
#             vals['service_order'] = self.env['ir.sequence'].next_by_code('maintenance.request.sequence') or _('New')
#         result = super(MaintenanceRequest, self).create(vals)
#         return result

