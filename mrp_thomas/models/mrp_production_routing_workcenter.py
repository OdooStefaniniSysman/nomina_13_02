from odoo import models, fields, api

class MrProductionRoutingWorkcenter(models.Model):
    _name = 'mrp.production.routing.workcenter'
    _description = 'Rutas de producción en la Órden de producción'

    name = fields.Char(string="Nombre")
    routing_production_id = fields.Many2one('mrp.production')
    routing_id = fields.Many2one('mrp.routing', string="Rutas")
    workcenter_id = fields.Many2one('mrp.workcenter', string="Centro de Producción")
    description = fields.Text(string="Observaciones")
    time_cycle = fields.Float(string="Duración")