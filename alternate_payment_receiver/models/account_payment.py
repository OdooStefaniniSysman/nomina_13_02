# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    activate_alternative_contact = fields.Boolean(string='Need alternative Receiver?', default=False)
    alternative_contact = fields.Char(string='Alternate Receiver of Payment')

    @api.onchange('activate_alternative_contact','partner_id')
    def onchange_activate_alternative_contact(self):
        if self.activate_alternative_contact:
            if not self.partner_id:
                self.activate_alternative_contact = False
                return {'warning': {'title': 'Warning!','message': 'Por favor seleccionar un tercero'}}
            else:
                if not self.partner_id.property_alternative_contact_id:
                    self.alternative_contact = ""
                    self.activate_alternative_contact = False
                    return {'warning': {'title': 'Warning!','message': 'El tercero no tiene un contacto alternativo asignado'}}
                else:
                    self.alternative_contact = self.partner_id.property_alternative_contact_id.name
    

