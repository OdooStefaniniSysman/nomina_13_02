# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class AccountAnaltyticSegment(models.Model):
    _name = 'account.analytic.segment'

    name = fields.Char('Nombre de Segmento')
    ref = fields.Char('Referencia')