import re
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class AccountJournaThomas(models.Model):
    _inherit = 'account.payment'
    
    check_number_thomas = fields.Char(string="Número de cheque", related="journal_id.sequence_concatenation")