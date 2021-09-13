# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountAccount(models.Model):
    _inherit = 'account.account'

    colgap_account_ok = fields.Boolean('COLGAP Account',
        help='By default Odoo accounting reflects IFRS standards, check this box to indicate that the account behaves locally(COLPGAP)')

    niff_account_ok = fields.Boolean('NIFF Account',
        help='By default Odoo accounting reflects IFRS standards, check this box to indicate that the account behaves NIFF')
