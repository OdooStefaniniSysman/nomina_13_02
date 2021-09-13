# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class AccountAnaltyticAccountInherit(models.Model):
    _inherit = 'account.analytic.account'

    segment_id = fields.Many2one('account.analytic.segment', string="Segmento de operaciones")
    ceco_sap = fields.Char('CeCo SAP')