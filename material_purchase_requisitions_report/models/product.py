from odoo import models, fields, api
import odoo.addons.decimal_precision as dp

class ProductCategoryInherit(models.Model):
    _inherit = 'product.category'

    account_internal_id = fields.Many2one('account.account', 'Cuenta de consumo Interno', company_dependent=True, domain="['&', ('deprecated', '=', False), ('company_id', '=', current_company_id)]")
