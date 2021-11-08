from odoo import api, fields, models, _, SUPERUSER_ID
from odoo.exceptions import Warning


class AccountJournal(models.Model):
    _inherit = 'account.journal'


    is_ut = fields.Boolean(string="¿is UT?", default=False)
    alternate_partner_id = fields.Many2one(
        string="Partner",
        comodel_name="res.partner",
        domain="['|',('company_id', '=', company_id),('company_id', '=', False)]",
        help="Conctact used in UT payments",
    )