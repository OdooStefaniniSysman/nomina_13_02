from odoo import api, fields, models, _

class PaymentType(models.Model):
    _name = 'payment.type'
    _description = 'Payment Type'

    name = fields.Char(string='Name')
    code = fields.Char(string='Code')
    active = fields.Boolean(default=True)

    _sql_constraints = [
		('name_unique', 'unique(name)', _("The name must be unique")),
		('code_unique', 'unique(code)', _("The code must be unique"))]
    
