# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResUsersSignature(models.Model):
    _name = 'res.users.signature'
    _description = 'Res Users Signature'

    company_id = fields.Many2one('res.company', 'Company')
    user_id = fields.Many2one('res.users', 'User', required=True)
    signature = fields.Html('Email Signature')

    _sql_constraints = [
        ('email_unique',
         'UNIQUE(company_id,user_id,signature)',
         "The signature must be unique per user and company"),
    ]


class ResUsers(models.Model):
    _inherit = 'res.users'

    def _get_users_signature(self):
        for user in self:
            domain = [('company_id','=',self.env.companies[0].id),('user_id','=',user.id)]
            user.signature = self.env['res.users.signature'].search(domain).signature

    def _set_users_signature(self):
        for user in self:
            domain = [('company_id','=',self.env.companies[0].id),('user_id','=',user.id)]
            signature = self.env['res.users.signature'].search(domain)
            if signature:
                signature.write({'signature': user.signature})
            else:
                vals = {
                    'company_id': self.env.companies[0].id,
                    'user_id': user.id,
                    'signature': user.signature,
                }
                self.env['res.users.signature'].create(vals)

    signature = fields.Html(compute='_get_users_signature', inverse='_set_users_signature')
