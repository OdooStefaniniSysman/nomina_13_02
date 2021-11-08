#Luis Felipe Paternina--
# Ingeniero de Sistemas
#Todoo SAS
from odoo import models, fields, api

class Todoo(models.Model):
    _inherit = 'maintenance.equipment'

    brand_maintenance = fields.Char(string="Marca", trackinig=True)
    date_start_contract = fields.Date(related="partner_id.start_date_contract", string="Fecha Inicio de Contrato", trackinig=True)
    date_end = fields.Date(related="partner_id.end_date_contract", string="Fecha Fin de Contrato",trackinig=True)
    maintenance_value = fields.Integer(string="Valor del Mantenimiento Preventivo", tracking=True)
    maintenance_cant = fields.Integer(string="Cantidad de Mantenimientos", tracking=True)
    maintenance_total = fields.Integer(string="Valor Total del Mantenimiento", compute="_calculate_maintenance_total")
    maintenance_frequency = fields.Integer(string="Frecuencia del Mantenimiento", tracking=True)
    branch = fields.Many2one('res.city', string="Ciudad", tracking=True)
    inventory_plate = fields.Char(string="Placa de Inventario")
    address = fields.Char(string="Dirección de Sucursal")
    office_code = fields.Char(string="Código de Oficina - Sucursal")
    department = fields.Many2one('res.country.state', string="Departamento")
    branch_tst = fields.Char(string="Sucursal")
    maintenance_value_corrective = fields.Integer(string="Valor del Mantenimiento Correctivo")
    rental_contract = fields.Boolean(string="Máquina en Contrato de Alquiler")
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
    
    #Calcular total del matenimiento
    @api.depends('maintenance_cant','maintenance_value')
    def _calculate_maintenance_total(self):
        for record in self:
            record.maintenance_total = record.maintenance_cant * record.maintenance_value

    def action_view_stock_move_lines(self):
        self.ensure_one()
        action = self.env.ref('stock.stock_move_line_action').read()[0]
        lot_ids = self.env['stock.production.lot'].search([('name','=',self.serial_no)])
        if lot_ids:
            lot_ids = lot_ids.ids
        else:
            lot_ids = []    
        action['domain'] = [('lot_id', 'in', lot_ids)]
        return action

      
        