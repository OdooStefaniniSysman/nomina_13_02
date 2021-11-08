# -*- coding: utf-8 -*-

from odoo import models, fields, api


class HelpdeskStage(models.Model):
    _inherit = 'helpdesk.stage'

    company_id = fields.Many2one('res.company', 'Company')


class HelpdeskTag(models.Model):
    _inherit = 'helpdesk.tag'

    company_id = fields.Many2one('res.company', 'Company')
