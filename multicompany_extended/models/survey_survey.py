# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SurveySurvey(models.Model):
    _inherit = 'survey.survey'

    company_id = fields.Many2one('res.company', 'Company')
