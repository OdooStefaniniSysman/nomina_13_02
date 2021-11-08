# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging
import poplib
from imaplib import IMAP4, IMAP4_SSL
from poplib import POP3, POP3_SSL

from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError


_logger = logging.getLogger(__name__)
MAX_POP_MESSAGES = 50
MAIL_TIMEOUT = 60
class FetchmailServer(models.Model):
    """Incoming POP/IMAP mail server account"""

    _inherit = 'fetchmail.server'
    
    @api.model
    def _fetch_mails(self,server_alias=None):
        """ Method called by cron to fetch mails from servers """
        
        if not server_alias:
            return self.search([('state', '=', 'done'), ('server_type', 'in', ['pop', 'imap'])]).fetch_mail()
        else:
            return self.search([('state', '=', 'done'), ('user','ilike',server_alias), ('server_type', 'in', ['pop', 'imap'])]).fetch_mail()