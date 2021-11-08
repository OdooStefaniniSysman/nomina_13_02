# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class AssetSell(models.TransientModel):
    _inherit = 'account.asset.sell'
   
    action = fields.Selection(selection_add=[('mantenido_venta', 'Mantenido para la venta'),('propiedad_inversion', 'Propiedad de inversion')])
    asset_type = fields.Selection([('sale', 'Sale: Revenue Recognition'), ('purchase', 'Purchase: Asset'), ('expense', 'Deferred Expense')], index=True, readonly=False,  related='asset_id.asset_type')
    user_type_id = fields.Many2one('account.account.type', related="asset_id.user_type_id", string="Type of the account")
    model_id = fields.Many2one('account.asset', string='Asset Model', change_default=True)

    asset_account_id = fields.Many2one('account.account', string='Cuenta del activo',domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]", related='model_id.account_asset_id_niff')
    depreciation_account_id = fields.Many2one('account.account', string='Cuenta depreciacion',domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]", related='model_id.account_depreciation_id_niff')
    

    def do_action_niff(self):
        self.ensure_one()
        # invoice_line = self.env['account.move.line'] if self.action == 'dispose' else self.invoice_line_id or self.invoice_id.invoice_line_ids
        invoice_line = self.env['account.move.line'] 
        return self.asset_id.set_to_close_niff(invoice_line_id=invoice_line, date=invoice_line.move_id.invoice_date, action=self.action, model_id=self.model_id)