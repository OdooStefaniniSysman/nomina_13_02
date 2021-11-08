from odoo import fields, api, models

class ResPartner(models.Model):
    _inherit = 'res.partner'

    invoice_condition = fields.Text('Invoice Condition',required=False)
