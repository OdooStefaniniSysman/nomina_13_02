# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

class ResCompany(models.Model):
    _inherit = 'res.company'

    alias_domain_inh = fields.Char('Alias Domain')
    external_email_server_default_inh = fields.Boolean("External Email Servers")

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    
    external_email_server_default = fields.Boolean(
        "External Email Servers",related="company_id.external_email_server_default_inh" , readonly=False,
        config_parameter='base_setup.default_external_email_server')
    alias_domain = fields.Char('Alias Domain',related="company_id.alias_domain_inh" ,readonly=False,help="If you have setup a catch-all email domain redirected to "

                               "the Odoo server, enter the domain name here.", config_parameter='mail.catchall.domain')

    
    
    