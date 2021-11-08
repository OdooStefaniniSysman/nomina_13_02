from odoo import api, fields, models, _


class MrpRoutingth(models.Model):
    """ Specifies routings of work centers """
    _inherit = 'mrp.routing'
    _description = 'Routings'

    description_thomas = fields.Text(string="Observaciones")
    

class MrpRoutingWorkcenterth(models.Model):
    _inherit = 'mrp.routing.workcenter'
   
    