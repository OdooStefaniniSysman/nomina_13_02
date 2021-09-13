from odoo import api, fields, models, _, SUPERUSER_ID
from odoo.exceptions import Warning
from odoo.tools import float_compare, float_is_zero, float_round


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    def get_line(self,amount, account, partner):
            account_analytic_id = self.analytic_account_id
            company_currency = self.company_id.currency_id
            current_currency = self.currency_id
            prec = company_currency.decimal_places
            return (0, 0, {
                'name': 'Cruce UT',
                'account_id': account.id,
                'partner_id': partner.id,
                'debit': 0.0 if float_compare(amount, 0.0, precision_digits=prec) > 0 else -amount,
                'credit': amount if float_compare(amount, 0.0, precision_digits=prec) > 0 else 0.0,
                'analytic_account_id': account_analytic_id.id,
                'currency_id': company_currency != current_currency and current_currency.id or False,
                'amount_currency': company_currency != current_currency and - 1.0 * amount or 0.0,
            })

    def post(self):
        # configs = self.env['res.config.settings'].search([])
        # co = configs.mapped('module_inter_company_rules')
        # config = co[-1]
        # if config:
        companies = self.env['res.company'].search([]).mapped('partner_id')
        receiver = self.partner_id
        journal_ut = False
        # if self.journal_id.name.find(' UT ') >= 0:
        #     journal_ut = self.env['account.journal'].sudo().search([('company_id','!=',self.company_id.id), ('name','=',self.journal_id.name),('type','=','bank')])
        if self.journal_id.is_ut and self.payment_type == 'outbound':
            journal_ut = self.env['account.journal'].sudo().search([('company_id','!=',self.company_id.id), ('name','=',self.journal_id.name),('type','=','bank')])
            company = journal_ut.company_id
            line_datas = [(-self.amount, journal_ut.default_debit_account_id, company.partner_id),
                        # (self.amount, company.partner_id.with_context(force_company=company.id).property_account_receivable_id, self.company_id.partner_id)]
                        (self.amount, journal_ut.default_debit_account_id, self.company_id.partner_id)]
            vals = {
                    'amount_total': abs(self.amount),
                    # 'name':self.communication or 'Cruce UT',
                    'ref': self.communication or 'Cruce UT',
                    'date': fields.Date.today(),
                    'type': 'entry',
                    'currency_id': self.currency_id.id,
                    'journal_id': journal_ut.id,
                    'company_id': company.id,
                    'line_ids': [self.get_line(amount, account, partner) for amount, account, partner in line_datas if account],
                }
            move = self.env['account.move'].with_context(company=company.id)
            move.sudo().create(vals)
        elif receiver in companies:
            company = self.env['res.company'].search([('name','=',self.partner_id.name)])
            if self.partner_type == 'customer' and self.payment_type == 'inbound':
                payment_type = 'outbound'
                # company = self.env['res.company'].search([('name','=',self.partner_id.name)])
                journal_id = self.env['account.journal'].sudo().search([('company_id','=',company.id)])
                vals = {
                    'payment_type': payment_type,
                    'partner_type': 'supplier',
                    'partner_id': self.company_id.partner_id.id,
                    'amount': self.amount,
                    'currency_id': self.currency_id.id,
                    'payment_date': self.payment_date,
                    'communication': self.communication,
                    'payment_method_id': self.payment_method_id.id,
                    'journal_id': journal_id[0].id
                }
                acco = self.env['account.payment'].with_context(company=company.id)
                account= acco.sudo().create(vals)
            elif self.partner_type == 'supplier' and self.payment_type == 'outbound':
                payment_type = 'inbound'
                # company = self.env['res.company'].search([('name','=',self.partner_id.name)])
                journal_id = self.env['account.journal'].sudo().search([('company_id','=',company.id)])
                vals = {
                    'payment_type': payment_type,
                    'partner_type': 'customer',
                    'partner_id': self.company_id.partner_id.id,
                    'amount': self.amount,
                    'currency_id': self.currency_id.id,
                    'payment_date': self.payment_date,
                    'communication': self.communication,
                    'payment_method_id': self.payment_method_id.id,
                    'journal_id': journal_id[0].id
                }
                acco = self.env['account.payment'].with_context(company=company.id)
                account= acco.sudo().create(vals)
        return super(AccountPayment, self).post()


    def _prepare_payment_moves(self):
        all_move_vals = super(AccountPayment,self)._prepare_payment_moves()
        if self.journal_id.is_ut and self.payment_type == 'outbound':
            journal_ut = self.env['account.journal'].sudo().search([('company_id','!=',self.company_id.id), ('name','=',self.journal_id.name),('type','=','bank')])
            company = journal_ut.company_id
            for move in all_move_vals:
                line_ids = move.get('line_ids')
                for line in line_ids:
                    if line[2].get('credit') > 0:
                        line[2]['partner_id'] = company.partner_id.id
        return all_move_vals
