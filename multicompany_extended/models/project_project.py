# -*- coding: utf-8 -*-

from odoo import models, fields, api


class MailActivityType(models.Model):
    _inherit = 'mail.activity.type'

    company_id = fields.Many2one('res.company', 'Company')


class ProjectTags(models.Model):
    _inherit = 'project.tags'

    company_id = fields.Many2one('res.company', 'Company')


class ProjectTaskType(models.Model):
    _inherit = 'project.task.type'

    company_id = fields.Many2one('res.company', 'Company')
