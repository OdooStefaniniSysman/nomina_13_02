from odoo import models, fields, api

class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    kronos_id = fields.Many2one('data.sheet','Ficha de datos',compute = '_compute_kronos_id')

    def _compute_kronos_id(self):
        for record in self:
            kronos_id = False
            domain = [('name', '=', record.origin)]
            sale = self.env['sale.order'].search(domain)
            for order in sale:
                kronos_id = order.sheet_id
            record.kronos_id = kronos_id



