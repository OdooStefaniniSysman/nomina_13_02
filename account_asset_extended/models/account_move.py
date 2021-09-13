# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.tools import float_compare
from odoo.tools.misc import formatLang
from dateutil.relativedelta import relativedelta

class AccountMove(models.Model):
    _inherit = 'account.move'

    asset_clasification = fields.Selection([('NIFF','NIFF'),
                        ('FISCAL','FISCAL'),
                        ('dismantlement','DESMANTELAMIENTO'),
                        ('NIFF_sale','NIFF Venta'),
                        ('NIFF_disp','NIFF Dispuesto'),
                        ('FISCAL_sale','FISCAL Venta'),
                        ('FISCAL_disp','FISCAL Dispuesto'),
                        ('NIFF_move','NIFF cambio modelo'),
                        ('FISCAL_move','FISCAL cambio modelo'),
                        ('valorizacion_niff','Valorizacion'),
                        ('valorizacion_fiscal','Valorizacion'),],string='Asset Type', default='FISCAL')
    # account_asset_second_id = fields.Many2one('account.asset', string='asset', related='asset_id')


    def _auto_create_asset(self):
        create_list = []
        invoice_list = []
        auto_validate = []
        for move in self:
            if not move.is_invoice():
                continue

            for move_line in move.line_ids:
                if (
                    move_line.account_id
                    and (move_line.account_id.can_create_asset)
                    and move_line.account_id.create_asset != "no"
                    and not move.reversed_entry_id
                    and not (move_line.currency_id or move.currency_id).is_zero(move_line.price_total)
                    and not move_line.asset_id
                ):
                    if not move_line.name:
                        raise UserError(_('Journal Items of {account} should have a label in order to generate an asset').format(account=move_line.account_id.display_name))
                    vals = {
                        'name': move_line.name,
                        'company_id': move_line.company_id.id,
                        'currency_id': move_line.company_currency_id.id,
                        'original_move_line_ids': [(6, False, move_line.ids)],
                        'state': 'draft',
                        'acquisition_date': move.invoice_date,
                        'acquisition_date_niff': move.invoice_date,
                    }
                    model_id = move_line.account_id.asset_model
                    if model_id:
                        vals.update({
                            'model_id': model_id.id,
                        })
                    # esta funcion asigna un producto al activo si se especifica en la factira, adelas si el producto
                    # tiene asignado un "asset_parent_id" le asigna automaticamente los campos del padre al nuevo activo
                    product = move_line.product_id
                    if product:
                        vals['name'] = '[' + move_line.product_id.default_code + '] ' + move_line.product_id.name
                        if product.asset_template_parent_id:
                            asset_parent = self.env['account.asset'].search([('product_id','=', product.asset_template_parent_id.id)])
                            vals.update({
                                'asset_parent_id': asset_parent.id,
                                'product_id': product.product_tmpl_id.id,
                            })
                        else:
                            vals.update({
                                'product_id': product.product_tmpl_id.id,
                            })
                    auto_validate.append(move_line.account_id.create_asset == 'validate')
                    invoice_list.append(move)
                    create_list.append(vals)

        assets = self.env['account.asset'].create(create_list)
        for asset, vals, invoice, validate in zip(assets, create_list, invoice_list, auto_validate):
            if 'model_id' in vals and not 'asset_parent_id' in vals:
                asset._onchange_model_id()
                asset._onchange_method_period()
                if validate:
                    asset.validate()
            if 'asset_parent_id' in vals:
                asset.onchange_asset_parent_id()
            if invoice:
                asset_name = {
                    'purchase': _('Asset'),
                    'sale': _('Deferred revenue'),
                    'expense': _('Deferred expense'),
                }[asset.asset_type]
                msg = _('%s created from invoice') % (asset_name)
                msg += ': <a href=# data-oe-model=account.move data-oe-id=%d>%s</a>' % (invoice.id, invoice.name)
                asset.message_post(body=msg)
        return assets

    #funcion para calcular lineas teniendo en cuenta los campos NIFF
    @api.model
    def _prepare_move_for_asset_depreciation_niff(self, vals):
        missing_fields = set(['asset_id', 'move_ref', 'amount', 'asset_remaining_value', 'asset_depreciated_value']) - set(vals)
        if missing_fields:
            raise UserError(_('Some fields are missing {}').format(', '.join(missing_fields)))
        asset = vals['asset_id']
        account_analytic_id = asset.account_analytic_id
        analytic_tag_ids = asset.analytic_tag_ids_niff
        depreciation_date = vals.get('date', fields.Date.context_today(self))
        company_currency = asset.company_id.currency_id
        current_currency = asset.currency_id
        prec = company_currency.decimal_places
        amount = current_currency._convert(vals['amount'], company_currency, asset.company_id, depreciation_date)
        move_line_1 = {
            'name': asset.name,
            'account_id': asset.account_depreciation_id_niff.id,
            # 'partner_id': self.env.company.id,
            'debit': 0.0 if float_compare(amount, 0.0, precision_digits=prec) > 0 else -amount,
            'credit': amount if float_compare(amount, 0.0, precision_digits=prec) > 0 else 0.0,
            'analytic_account_id': account_analytic_id.id if asset.asset_type == 'sale' else False,
            'analytic_tag_ids': [(6, 0, analytic_tag_ids.ids)] if asset.asset_type == 'sale' else False,
            'currency_id': company_currency != current_currency and current_currency.id or False,
            'amount_currency': company_currency != current_currency and - 1.0 * vals['amount'] or 0.0,
        }
        move_line_2 = {
            'name': asset.name,
            'account_id': asset.account_depreciation_expense_id_niff.id,
            # 'partner_id': self.env.company.id,
            'credit': 0.0 if float_compare(amount, 0.0, precision_digits=prec) > 0 else -amount,
            'debit': amount if float_compare(amount, 0.0, precision_digits=prec) > 0 else 0.0,
            'analytic_account_id': account_analytic_id.id if asset.asset_type in ('purchase', 'expense') else False,
            'analytic_tag_ids': [(6, 0, analytic_tag_ids.ids)] if asset.asset_type in ('purchase', 'expense') else False,
            'currency_id': company_currency != current_currency and current_currency.id or False,
            'amount_currency': company_currency != current_currency and vals['amount'] or 0.0,
        }
        move_vals = {
            'ref': vals['move_ref'],
            'date': depreciation_date,
            'journal_id': asset.journal_id_niff.id,
            'line_ids': [(0, 0, move_line_1), (0, 0, move_line_2)],
            'auto_post': asset.state == 'open',
            'asset_id': asset.id,
            'asset_remaining_value': vals['asset_remaining_value'],
            'asset_depreciated_value': vals['asset_depreciated_value'],
            'amount_total': amount,
            'name': '/',
            'asset_value_change': vals.get('asset_value_change', False),
            'type': 'entry',
            'currency_id': current_currency.id,
            'asset_clasification': 'NIFF',
        }
        return move_vals

    
    def _depreciate(self):
        # se reescribe la funcion ya que ahora toca tener en cuenta la calsificacion del movimiento, si es NIFF o FISCAL
        for move in self.filtered(lambda m: m.asset_id):
            asset = move.asset_id
            if asset.state in ('open', 'pause') or asset.both_paused or asset.niff_paused or asset.fiscal_paused:
                # asset.value_residual -= abs(sum(move.line_ids.filtered(lambda l: l.account_id == asset.account_depreciation_id and move.asset_clasification == 'FISCAL').mapped('balance')))
                # asset.value_residual_niff -= abs(sum(move.line_ids.filtered(lambda l: l.account_id == asset.account_depreciation_id_niff and move.asset_clasification == 'NIFF').mapped('balance')))
                asset.value_residual -= abs(move.amount_total if move.asset_clasification == 'FISCAL' and move.state == 'posted' else 0)
                asset.value_residual_niff -= abs(move.amount_total if move.asset_clasification == 'NIFF' and move.state == 'posted' else 0)
            elif asset.state == 'close':
                # asset.value_residual -= abs(sum(move.line_ids.filtered(lambda l: l.account_id != asset.account_depreciation_id and move.asset_clasification == 'FISCAL').mapped('balance')))
                # asset.value_residual_niff -= abs(sum(move.line_ids.filtered(lambda l: l.account_id != asset.account_depreciation_id_niff and move.asset_clasification == 'NIFF').mapped('balance')))
                asset.value_residual -= abs(move.amount_total if move.asset_clasification == 'FISCAL' and move.state == 'posted' else 0)
                asset.value_residual_niff -= abs(move.amount_total if move.asset_clasification == 'NIFF' and move.state == 'posted' else 0)
            else:
                raise UserError(_('You cannot post a depreciation on an asset in this state: %s') % dict(self.env['account.asset']._fields['state'].selection)[asset.state])


    # @api.model
    # def _prepare_move_for_asset_depreciation(self, vals):
    #     move = super(AccountMove,self)._prepare_move_for_asset_depreciation(vals)
    #     line_ids = move.get('line_ids')
    #     for line in line_ids:
    #         line[2]['partner_id'] = self.env.company.id
    #     return move