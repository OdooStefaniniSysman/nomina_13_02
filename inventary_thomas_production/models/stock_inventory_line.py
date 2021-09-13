from odoo import _, api, fields, models


class StockInventoryLine(models.Model):
    _inherit = 'stock.inventory.line'

    diff_motive = fields.Char('Difference Reason')