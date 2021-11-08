# -*- coding: utf-8 -*-
from odoo import api, fields, models, _, SUPERUSER_ID
from odoo.exceptions import Warning


class res_company(models.Model):
    _inherit = 'res.company'

    rule_type = fields.Selection(selection_add=[('cu_and_sup', 'Synchronize payments Customer/Supplier')])