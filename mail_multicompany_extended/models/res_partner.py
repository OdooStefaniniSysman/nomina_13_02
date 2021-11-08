# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResPartnerEmail(models.Model):
    _name = 'res.partner.email'
    _description = 'Res Partner Email'

    company_id = fields.Many2one('res.company', 'Company')
    partner_id = fields.Many2one('res.partner', 'Partner', required=True)
    email = fields.Char('Email')

    _sql_constraints = [
        ('email_unique',
         'UNIQUE(company_id,partner_id,email)',
         "The email must be unique per partner and company"),
    ]


class ResPartner(models.Model):
    _inherit = 'res.partner'

    def _get_partner_email(self):
        for partner in self:
            company = partner.company_id if partner.company_id else self.env.companies[0]
            domain = [('company_id','=',company.id),('partner_id','=',partner.id)]
            partner.email = self.env['res.partner.email'].search(domain).email

    def _set_partner_email(self):
        for partner in self:
            domain = [('company_id','=',self.env.companies[0].id),('partner_id','=',partner.id)]
            email = self.env['res.partner.email'].search(domain)
            if email:
                email.write({'email': partner.email})
            else:
                company = partner.company_id if partner.company_id else self.env.companies[0]
                vals = {
                    'company_id': company.id,
                    'partner_id': partner.id,
                    'email': partner.email,
                }
                self.env['res.partner.email'].create(vals)

    email = fields.Char(compute='_get_partner_email', inverse='_set_partner_email')
