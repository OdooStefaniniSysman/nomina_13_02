from odoo import models, api, fields

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    delivery_id = fields.Many2one('res.users','Delivery By')
    recieved_id = fields.Many2one('res.users','Decieved By')
    owner_id = fields.Many2one('res.users','Owner')
    security_aux_id = fields.Many2one('res.users','Security Auxiliar')
    area = fields.Char('Solicitant Area',compute='_compute_area')
    responsable = fields.Char('Responsable',compute='_compute_responsable')
    charge_to = fields.Char('Charge To',compute='_compute_charge_to')
    cost_center_id = fields.Many2one('mrp.workcenter','Cost Center')
    
    
    def _compute_area(self):
        for record in self:
            if record.custom_requisition_id:
                record.area = record.custom_requisition_id.department_id.name
            else:
                record.area = ''
                
    def _compute_responsable(self):
        for record in self:
            if record.custom_requisition_id:
                record.responsable = record.custom_requisition_id.employee_id.name
            else:
                record.responsable = ''

    def _compute_charge_to(self):
        for record in self:
            if record.custom_requisition_id:
                record.charge_to = record.custom_requisition_id.charge_to
            else:
                record.charge_to = ''