# Copyright 2020-TODAY Miguel Pardo <ing.miguel.pardo@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class HrEmployee(models.Model):
    """Add Is Foreign."""
    _inherit = "hr.employee"

    is_foreign = fields.Boolean(tracking=True)
    ccf_id = fields.Many2one(
        'res.partner', 'CCF',
        domain="[('is_compensation_box', '=', True)]",
        tracking=True)
