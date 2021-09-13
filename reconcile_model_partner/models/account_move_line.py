# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'


    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            model_id = vals.get('reconcile_model_id')
            partner = vals.get('partner_id') 
            if not partner and model_id:
                model = self.env['account.reconcile.model'].browse(model_id)
                if model.has_second_line and model.second_account_id.id == vals.get('account_id') and model.second_label == vals.get('name') and ((model.second_analytic_account_id.id == vals.get('analytic_account_id') if vals.get('analytic_account_id') else True)):
                    vals['partner_id'] = model.second_partner_id.id
                else:
                    vals['partner_id'] = model.partner_id.id
                if model.analytic_account_id.id == vals.get('analytic_account_id'):
                    print('aca')
        return super(AccountMoveLine, self).create(vals_list)
