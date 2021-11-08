# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import RedirectWarning, UserError, ValidationError, AccessError, Warning


class AccountMove(models.Model):
    _inherit = 'account.move'

    application_number = fields.Char(string='N° Solicitud')