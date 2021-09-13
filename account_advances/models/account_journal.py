# -*- coding: utf-8 -*-

from odoo import fields, models, api


class AccountJournal(models.Model):
    _inherit = 'account.journal'

    advance_assign_ok = fields.Boolean(string='Allowed for Crossing Advances?')
