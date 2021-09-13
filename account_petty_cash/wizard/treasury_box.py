# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, _
from odoo.exceptions import UserError

from odoo.addons.account.wizard.pos_box import CashBox


class TreasuryBox(CashBox):
    _register = False

    def run(self):
        active_model = self.env.context.get('active_model', False)
        active_ids = self.env.context.get('active_ids', [])

        if active_model == 'treasury.session':
            bank_statements = [session.cash_register_id for session in self.env[active_model].browse(active_ids) if session.cash_register_id]
            if not bank_statements:
                raise UserError(_("No hay caja registradora para esta sesión de Caja Menor"))
            return self._run(bank_statements)
        else:
            return super(TreasuryBox, self).run()


class TreasuryBoxOut(TreasuryBox):
    _inherit = 'cash.box.out'

    def _calculate_values_for_statement_line(self, record):
        values = super(TreasuryBoxOut, self)._calculate_values_for_statement_line(record)
        active_model = self.env.context.get('active_model', False)
        active_ids = self.env.context.get('active_ids', [])
        if active_model == 'treasury.session' and active_ids:
            values['ref'] = self.env[active_model].browse(active_ids)[0].name
        return values
