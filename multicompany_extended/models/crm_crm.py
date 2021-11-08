# -*- coding: utf-8 -*-

from odoo import models, fields, api


class CrmLeadTag(models.Model):
    _inherit = 'crm.lead.tag'

    company_id = fields.Many2one('res.company', 'Company')


class CrmLostReason(models.Model):
    _inherit = 'crm.lost.reason'

    company_id = fields.Many2one('res.company', 'Company')


class CrmStage(models.Model):
    _inherit = 'crm.stage'

    company_id = fields.Many2one('res.company', 'Company')
