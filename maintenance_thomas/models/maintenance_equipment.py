from odoo import models,fields,api

class MaintenanceEquipment(models.Model):
    _inherit = 'maintenance.equipment'

    image = fields.Binary()
    velocity = fields.Char('Velocity')
    capacity = fields.Char('Capacity')
    maker = fields.Char('Maker')
    origin = fields.Char('Origin Country')
    fabrication_date = fields.Date('Fabrication Year')
    machine_type = fields.Char('Machine Type')
    phone = fields.Char('Phone')
    voltage_connection = fields.Char('Voltage Connection')
    intake = fields.Char('Intake')
    power = fields.Char('Power')
    compressed_air = fields.Char('Compressed Air')
    water = fields.Char('Water')
    conditioning_air = fields.Char('Conditioning Air')
    observation = fields.Text('Observations')
    internal_code = fields.Char('Internal Code')
    connection = fields.Boolean()
    requirement = fields.Boolean()
