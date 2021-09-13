# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import time
import json
import io
from odoo import models, api, fields, _
from odoo.tools.misc import format_date
from odoo.exceptions import UserError
from odoo.tools import float_is_zero
from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo.tools.misc import xlsxwriter

class report_account_aged_partner(models.AbstractModel):
    _inherit = "account.aged.partner"


    def _get_columns_name(self, options):
        comparison = self._context.get('comparison', False)
        if comparison:
            date_comparison = (datetime.strptime(self._context['date_to'], '%Y-%m-%d').date()) - relativedelta(days=30)
            columns = [
                {},
                {'name': _("Partner name"), 'class': '', 'style': 'text-align:left; white-space:nowrap;'},
                {'name': _("Doc Number"), 'class': '', 'style': 'white-space:nowrap;'},
                {'name': _("Due Date"), 'class': 'date', 'style': 'white-space:nowrap;'},
                {'name': _("Journal"), 'class': '', 'style': 'text-align:center; white-space:nowrap;'},
                {'name': _("Account"), 'class': '', 'style': 'text-align:center; white-space:nowrap;'},
                {'name': _("Reference"), 'class': '', 'style': 'text-align:center; white-space:nowrap;'},
                {'name': _("Prev As of: %s") % format_date(self.env, date_comparison), 'class': 'number sortable', 'style': 'white-space:nowrap;'},
                {'name': _("As of: %s") % format_date(self.env, options['date']['date_to']), 'class': 'number sortable', 'style': 'white-space:nowrap;'},
                {'name': _("Prev 1 - 30"), 'class': 'number sortable', 'style': 'white-space:nowrap;'},
                {'name': _("1 - 30"), 'class': 'number sortable', 'style': 'white-space:nowrap;'},
                {'name': _("Prev 31 - 60"), 'class': 'number sortable', 'style': 'white-space:nowrap;'},
                {'name': _("31 - 60"), 'class': 'number sortable', 'style': 'white-space:nowrap;'},
                {'name': _("Prev 61 - 90"), 'class': 'number sortable', 'style': 'white-space:nowrap;'},
                {'name': _("61 - 90"), 'class': 'number sortable', 'style': 'white-space:nowrap;'},
                {'name': _("Prev 91 - 120"), 'class': 'number sortable', 'style': 'white-space:nowrap;'},
                {'name': _("91 - 120"), 'class': 'number sortable', 'style': 'white-space:nowrap;'},
                {'name': _("Prev 121 - 180"), 'class': 'number sortable', 'style': 'white-space:nowrap;'},
                {'name': _("121 - 180"), 'class': 'number sortable', 'style': 'white-space:nowrap;'},
                {'name': _("Prev 181 - 360"), 'class': 'number sortable', 'style': 'white-space:nowrap;'},
                {'name': _("181 - 360"), 'class': 'number sortable', 'style': 'white-space:nowrap;'},
                {'name': _("Prev Older"), 'class': 'number sortable', 'style': 'white-space:nowrap;'},
                {'name': _("Older"), 'class': 'number sortable', 'style': 'white-space:nowrap;'},
                {'name': _("Prev Total"), 'class': 'number sortable', 'style': 'white-space:nowrap;'},
                {'name': _("Total"), 'class': 'number sortable', 'style': 'white-space:nowrap;'},
            ]
        else:
            columns = [
                {},
                {'name': _("Partner name"), 'class': '', 'style': 'text-align:left; white-space:nowrap;'},
                {'name': _("Doc Number"), 'class': '', 'style': 'white-space:nowrap;'},
                {'name': _("Industry"), 'class': '', 'style': 'white-space:nowrap;'},
                {'name': _("Date"), 'class': 'date', 'style': 'white-space:nowrap;'},
                {'name': _("Due Date"), 'class': 'date', 'style': 'white-space:nowrap;'},
                {'name': _("Due days"), 'class': '', 'style': 'text-align:center; white-space:nowrap;'},
                {'name': _("Rad. Partner"), 'class': '', 'style': 'text-align:center; white-space:nowrap;'},
                {'name': _("Rad. Portfolio"), 'class': '', 'style': 'text-align:center; white-space:nowrap;'},
                {'name': _("Journal"), 'class': '', 'style': 'text-align:center; white-space:nowrap;'},
                {'name': _("Account"), 'class': '', 'style': 'text-align:center; white-space:nowrap;'},
                {'name': _("Reference"), 'class': '', 'style': 'text-align:center; white-space:nowrap;'},
                {'name': _("Tags"), 'class': '', 'style': 'text-align:center; white-space:nowrap;'},
                {'name': _("Exp. Date"), 'class': 'date', 'style': 'white-space:nowrap;'},
                {'name': _("As of: %s") % format_date(self.env, options['date']['date_to']), 'class': 'number sortable', 'style': 'white-space:nowrap;'},
                {'name': _("1 - 30"), 'class': 'number sortable', 'style': 'white-space:nowrap;'},
                {'name': _("31 - 60"), 'class': 'number sortable', 'style': 'white-space:nowrap;'},
                {'name': _("61 - 90"), 'class': 'number sortable', 'style': 'white-space:nowrap;'},
                {'name': _("91 - 120"), 'class': 'number sortable', 'style': 'white-space:nowrap;'},
                {'name': _("121 - 180"), 'class': 'number sortable', 'style': 'white-space:nowrap;'},
                {'name': _("181 - 360"), 'class': 'number sortable', 'style': 'white-space:nowrap;'},
                {'name': _("Older"), 'class': 'number sortable', 'style': 'white-space:nowrap;'},
                {'name': _("Total"), 'class': 'number sortable', 'style': 'white-space:nowrap;'},
            ]
        return columns


    @api.model
    def _get_lines(self, options, line_id=None):
        sign = -1.0 if self.env.context.get('aged_balance') else 1.0
        lines = []
        p_total = False
        account_types = [self.env.context.get('account_type')]
        context = {'include_nullified_amount': True}
        comparison = self._context.get('comparison', False)
        if line_id and 'partner_' in line_id:
            # we only want to fetch data about this partner because we are expanding a line
            context.update(partner_ids=self.env['res.partner'].browse(int(line_id.split('_')[1])))
        results, total, amls = self.env['report.account.report_agedpartnerbalance'].with_context(**context)._get_partner_move_lines(account_types, self._context['date_to'], 'posted', 30)


        for values in results:
            partner = self.env['res.partner'].browse(values['partner_id'])

            if comparison:
                date_comparison = (datetime.strptime(self._context['date_to'], '%Y-%m-%d').date()) - relativedelta(days=30)
                results_no, p_total, amls_no = self.env['report.account.report_agedpartnerbalance'].with_context(**context)._get_partner_move_lines(account_types, date_comparison, 'posted', 30)

                context_comparison = dict({'partner_ids': partner}, **context)
                p_results, total_no, p_amls = self.env['report.account.report_agedpartnerbalance'].with_context(**context_comparison)._get_partner_move_lines(account_types, date_comparison, 'posted', 30)
                for p_values in p_results:
                    value_comparison = {
                        'p_direction': p_values['direction'],
                        'p_0': p_values['0'],
                        'p_1': p_values['1'],
                        'p_2': p_values['2'],
                        'p_3': p_values['3'],
                        'p_4': p_values['4'],
                        'p_5': p_values['5'],
                        'p_6': p_values['6'],
                        'p_total': p_values['total']
                    }
                    values.update(value_comparison)

                vals = {
                    'id': 'partner_%s' % (values['partner_id'],),
                    'name': values['name'],
                    'level': 2,
                    'columns':
                        [{'name': ''}] * 6 +
                        [{'name': self.format_value(sign * v), 'no_format': sign * v}
                            for v in [
                                    values.get('p_direction', 0), values['direction'],
                                    values.get('p_6', 0), values['6'],
                                    values.get('p_5', 0), values['5'],
                                    values.get('p_4', 0), values['4'],
                                    values.get('p_3', 0), values['3'],
                                    values.get('p_2', 0), values['2'],
                                    values.get('p_1', 0), values['1'],
                                    values.get('p_0', 0),  values['0'],
                                    values.get('p_total', 0), values['total']
                            ]],
                    'trust': values['trust'],
                    'unfoldable': True,
                    'unfolded': 'partner_%s' % (values['partner_id'],) in options.get('unfolded_lines'),
                    'partner_id': values['partner_id'],
                }
                lines.append(vals)

                if 'partner_%s' % (values['partner_id'],) in options.get('unfolded_lines'):
                    if p_amls:
                        for line in p_amls[values['partner_id']]:
                            aml = line['line']
                            if aml.move_id.is_purchase_document():
                                caret_type = 'account.invoice.in'
                            elif aml.move_id.is_sale_document():
                                caret_type = 'account.invoice.out'
                            elif aml.payment_id:
                                caret_type = 'account.payment'
                            else:
                                caret_type = 'account.move'

                            line_date = aml.date_maturity or aml.date

                            vals = {
                                'id': aml.id,
                                'name': aml.move_id.name,
                                'class': 'date',
                                'caret_options': caret_type,
                                'level': 4,
                                'parent_id': 'partner_%s' % (values['partner_id'],),
                                'columns': [{'name': v} for v in [partner.name, partner.vat, format_date(self.env, aml.date_maturity or aml.date), aml.journal_id.code, aml.account_id.display_name, aml.move_id.ref]] +
                                        [{'name': self.format_value(sign * v, blank_if_zero=True), 'no_format': sign * v} for v in [((i % 2) == 0 and line['period'] == (8-(i//2))) and line['amount'] or 0 for i in range(18)]],
                                'action_context': {
                                    'default_type': aml.move_id.type,
                                    'default_journal_id': aml.move_id.journal_id.id,
                                },
                                'title_hover': self._format_aml_name(aml.name, aml.ref, aml.move_id.name),
                            }
                            lines.append(vals)

                    for line in amls[values['partner_id']]:
                        aml = line['line']
                        if aml.move_id.is_purchase_document():
                            caret_type = 'account.invoice.in'
                        elif aml.move_id.is_sale_document():
                            caret_type = 'account.invoice.out'
                        elif aml.payment_id:
                            caret_type = 'account.payment'
                        else:
                            caret_type = 'account.move'

                        line_date = aml.date_maturity or aml.date

                        vals = {
                            'id': aml.id,
                            'name': aml.move_id.name,
                            'class': 'date',
                            'caret_options': caret_type,
                            'level': 4,
                            'parent_id': 'partner_%s' % (values['partner_id'],),
                            'columns': [{'name': v} for v in [partner.name, partner.vat, format_date(self.env, aml.date_maturity or aml.date), aml.journal_id.code, aml.account_id.display_name, aml.move_id.ref]] +
                                    [{'name': self.format_value(sign * v, blank_if_zero=True), 'no_format': sign * v} for v in [((i % 2) != 0 and line['period'] == (8-(i//2))) and line['amount'] or 0 for i in range(18)]],
                            'action_context': {
                                'default_type': aml.move_id.type,
                                'default_journal_id': aml.move_id.journal_id.id,
                            },
                            'title_hover': self._format_aml_name(aml.name, aml.ref, aml.move_id.name),
                        }
                        lines.append(vals)

            else:
                vals = {
                    'id': 'partner_%s' % (values['partner_id'],),
                    'name': values['name'],
                    'level': 2,
                    'columns': [{'name': ''}] * 13 + [{'name': self.format_value(sign * v), 'no_format': sign * v}
                                                    for v in [values['direction'], values['6'],
                                                            values['5'], values['4'],
                                                            values['3'], values['2'],
                                                            values['1'], values['0'], values['total']]],
                    'trust': values['trust'],
                    'unfoldable': True,
                    'unfolded': 'partner_%s' % (values['partner_id'],) in options.get('unfolded_lines'),
                    'partner_id': values['partner_id'],
                }

                lines.append(vals)

                if 'partner_%s' % (values['partner_id'],) in options.get('unfolded_lines'):
                    for line in amls[values['partner_id']]:
                        aml = line['line']
                        if aml.move_id.is_purchase_document():
                            caret_type = 'account.invoice.in'
                        elif aml.move_id.is_sale_document():
                            caret_type = 'account.invoice.out'
                        elif aml.payment_id:
                            caret_type = 'account.payment'
                        else:
                            caret_type = 'account.move'

                        line_date = aml.date_maturity or aml.date
                        if not self._context.get('no_format'):
                            line_date = format_date(self.env, line_date)

                        due_days = (datetime.strptime(options['date']['date_to'], '%Y-%m-%d').date()) - (aml.date_maturity or aml.date)
                        rad_partner = aml.move_id.invoice_filed_customer
                        rad_portfolio = aml.move_id.invoice_filed_internally

                        vals = {
                            'id': aml.id,
                            'name': aml.move_id.name,
                            'class': 'date',
                            'caret_options': caret_type,
                            'level': 4,
                            'parent_id': 'partner_%s' % (values['partner_id'],),
                            'columns': [{'name': v} for v in [partner.name, partner.vat, partner.industry_id.name, format_date(self.env, aml.date), format_date(self.env, aml.date_maturity or aml.date), due_days.days, rad_partner, rad_portfolio, aml.journal_id.code, aml.account_id.display_name, aml.move_id.ref, ','.join(list(t.name for t in partner.category_id)), format_date(self.env, aml.expected_pay_date)]] +
                                    [{'name': self.format_value(sign * v, blank_if_zero=True), 'no_format': sign * v} for v in [line['period'] == 8-i and line['amount'] or 0 for i in range(9)]],
                            'action_context': {
                                'default_type': aml.move_id.type,
                                'default_journal_id': aml.move_id.journal_id.id,
                            },
                            'title_hover': self._format_aml_name(aml.name, aml.ref, aml.move_id.name),
                        }
                        lines.append(vals)

        if total and not line_id and not comparison:
            total_line = {
                'id': 0,
                'name': _('Total'),
                'class': 'total',
                'level': 2,
                'columns': [{'name': ''}] * 13 + [{'name': self.format_value(sign * v), 'no_format': sign * v} for v in [total[8], total[6], total[5], total[4], total[3], total[2], total[1], total[0], total[7]]],
            }
            lines.append(total_line)

        elif total and p_total and not line_id and comparison:
            total_line = {
                'id': 0,
                'name': _('Total'),
                'class': 'total',
                'level': 2,
                'columns': [{'name': ''}] * 6 + [{'name': self.format_value(sign * v), 'no_format': sign * v} for v in [p_total[8], total[8], p_total[6], total[6], p_total[5], total[5], p_total[4], total[4], p_total[3], total[3], p_total[2], total[2], p_total[1], total[1], p_total[0], total[0], p_total[7], total[7]]],
            }
            lines.append(total_line)
        return lines


class ReportAgedPartnerBalance(models.AbstractModel):
    _inherit = 'report.account.report_agedpartnerbalance'


    def _get_partner_move_lines(self, account_type, date_from, target_move, period_length):
        # This method can receive the context key 'include_nullified_amount' {Boolean}
        # Do an invoice and a payment and unreconcile. The amount will be nullified
        # By default, the partner wouldn't appear in this report.
        # The context key allow it to appear
        # In case of a period_length of 30 days as of 2019-02-08, we want the following periods:
        # Name       Stop         Start
        # 1 - 30   : 2019-02-07 - 2019-01-09
        # 31 - 60  : 2019-01-08 - 2018-12-10
        # 61 - 90  : 2018-12-09 - 2018-11-10
        # 91 - 120 : 2018-11-09 - 2018-10-11
        # +120     : 2018-10-10
        ctx = self._context
        periods = {}
        date_from = fields.Date.from_string(date_from)
        period_length_last = 150
        start = date_from
        qty_periods = 7
        for i in range(qty_periods)[::-1]:
            if i == 1:
                days = period_length + period_length_last
            elif i == 2:
                days = period_length * 2
            else:
                days = period_length
            stop = start - relativedelta(days=days)
            period_name = str((qty_periods-(i+1)) * period_length + 1) + '-' + str((qty_periods-i) * period_length)
            period_stop = (start - relativedelta(days=1)).strftime('%Y-%m-%d')
            if i == 0:
                period_name = '+' + str((qty_periods - 1) * period_length + period_length_last)
            if i == 1:
                period_name = str((qty_periods-(i+1)) * period_length + period_length + 1) + '-' + str((qty_periods-i) * period_length + period_length_last)
            if i == 2:
                period_name = str((qty_periods-(i+1)) * period_length + 1) + '-' + str((qty_periods-i) * period_length + period_length)
            periods[str(i)] = {
                'name': period_name,
                'stop': period_stop,
                'start': (i!=0 and stop.strftime('%Y-%m-%d') or False),
            }
            start = stop

        res = []
        total = []
        partner_clause = ''
        cr = self.env.cr
        user_company = self.env.company
        user_currency = user_company.currency_id
        company_ids = self._context.get('company_ids') or [user_company.id]
        move_state = ['draft', 'posted']
        if target_move == 'posted':
            move_state = ['posted']
        arg_list = (tuple(move_state), tuple(account_type), date_from, date_from,)
        if ctx.get('partner_ids'):
            partner_clause = 'AND (l.partner_id IN %s)'
            arg_list += (tuple(ctx['partner_ids'].ids),)
        if ctx.get('partner_categories'):
            partner_clause += 'AND (l.partner_id IN %s)'
            partner_ids = self.env['res.partner'].search([('category_id', 'in', ctx['partner_categories'].ids)]).ids
            arg_list += (tuple(partner_ids or [0]),)
        arg_list += (date_from, tuple(company_ids))

        query = '''
            SELECT DISTINCT l.partner_id, res_partner.name AS name, UPPER(res_partner.name) AS UPNAME, CASE WHEN prop.value_text IS NULL THEN 'normal' ELSE prop.value_text END AS trust
            FROM account_move_line AS l
              LEFT JOIN res_partner ON l.partner_id = res_partner.id
              LEFT JOIN ir_property prop ON (prop.res_id = 'res.partner,'||res_partner.id AND prop.name='trust' AND prop.company_id=%s),
              account_account, account_move am
            WHERE (l.account_id = account_account.id)
                AND (l.move_id = am.id)
                AND (am.state IN %s)
                AND (account_account.internal_type IN %s)
                AND (
                        l.reconciled IS FALSE
                        OR l.id IN(
                            SELECT credit_move_id FROM account_partial_reconcile where max_date > %s
                            UNION ALL
                            SELECT debit_move_id FROM account_partial_reconcile where max_date > %s
                        )
                    )
                    ''' + partner_clause + '''
                AND (l.date <= %s)
                AND l.company_id IN %s
            ORDER BY UPPER(res_partner.name)'''
        arg_list = (self.env.company.id,) + arg_list
        cr.execute(query, arg_list)
        partners = cr.dictfetchall()
        # put a total of 0
        for i in range(qty_periods+2):
            total.append(0)

        # Build a string like (1,2,3) for easy use in SQL query
        partner_ids = [partner['partner_id'] for partner in partners if partner['partner_id']]
        lines = dict((partner['partner_id'] or False, []) for partner in partners)
        if not partner_ids:
            return [], [], {}

        # Use one query per period and store results in history (a list variable)
        # Each history will contain: history[1] = {'<partner_id>': <partner_debit-credit>}
        history = []
        for i in range(qty_periods):
            args_list = (tuple(move_state), tuple(account_type), tuple(partner_ids),)
            dates_query = '(COALESCE(l.date_maturity,l.date)'

            if periods[str(i)]['start'] and periods[str(i)]['stop']:
                dates_query += ' BETWEEN %s AND %s)'
                args_list += (periods[str(i)]['start'], periods[str(i)]['stop'])
            elif periods[str(i)]['start']:
                dates_query += ' >= %s)'
                args_list += (periods[str(i)]['start'],)
            else:
                dates_query += ' <= %s)'
                args_list += (periods[str(i)]['stop'],)
            args_list += (date_from, tuple(company_ids))

            query = '''SELECT l.id
                    FROM account_move_line AS l, account_account, account_move am
                    WHERE (l.account_id = account_account.id) AND (l.move_id = am.id)
                        AND (am.state IN %s)
                        AND (account_account.internal_type IN %s)
                        AND ((l.partner_id IN %s) OR (l.partner_id IS NULL))
                        AND ''' + dates_query + '''
                    AND (l.date <= %s)
                    AND l.company_id IN %s
                    ORDER BY COALESCE(l.date_maturity, l.date)'''
            cr.execute(query, args_list)
            partners_amount = {}
            aml_ids = cr.fetchall()
            aml_ids = aml_ids and [x[0] for x in aml_ids] or []
            for line in self.env['account.move.line'].browse(aml_ids).with_context(prefetch_fields=False):
                partner_id = line.partner_id.id or False
                if partner_id not in partners_amount:
                    partners_amount[partner_id] = 0.0
                line_amount = line.company_id.currency_id._convert(line.balance, user_currency, user_company, date_from)
                if user_currency.is_zero(line_amount):
                    continue
                for partial_line in line.matched_debit_ids:
                    if partial_line.max_date <= date_from:
                        line_amount += partial_line.company_id.currency_id._convert(partial_line.amount, user_currency, user_company, date_from)
                for partial_line in line.matched_credit_ids:
                    if partial_line.max_date <= date_from:
                        line_amount -= partial_line.company_id.currency_id._convert(partial_line.amount, user_currency, user_company, date_from)

                if not self.env.company.currency_id.is_zero(line_amount):
                    partners_amount[partner_id] += line_amount
                    lines.setdefault(partner_id, [])
                    lines[partner_id].append({
                        'line': line,
                        'amount': line_amount,
                        'period': i + 1,
                        })
            history.append(partners_amount)

        # This dictionary will store the not due amount of all partners
        undue_amounts = {}
        query = '''SELECT l.id
                FROM account_move_line AS l, account_account, account_move am
                WHERE (l.account_id = account_account.id) AND (l.move_id = am.id)
                    AND (am.state IN %s)
                    AND (account_account.internal_type IN %s)
                    AND (COALESCE(l.date_maturity,l.date) >= %s)\
                    AND ((l.partner_id IN %s) OR (l.partner_id IS NULL))
                AND (l.date <= %s)
                AND l.company_id IN %s
                ORDER BY COALESCE(l.date_maturity, l.date)'''
        cr.execute(query, (tuple(move_state), tuple(account_type), date_from, tuple(partner_ids), date_from, tuple(company_ids)))
        aml_ids = cr.fetchall()
        aml_ids = aml_ids and [x[0] for x in aml_ids] or []
        for line in self.env['account.move.line'].browse(aml_ids):
            partner_id = line.partner_id.id or False
            if partner_id not in undue_amounts:
                undue_amounts[partner_id] = 0.0
            line_amount = line.company_id.currency_id._convert(line.balance, user_currency, user_company, date_from)
            if user_currency.is_zero(line_amount):
                continue
            for partial_line in line.matched_debit_ids:
                if partial_line.max_date <= date_from:
                    line_amount += partial_line.company_id.currency_id._convert(partial_line.amount, user_currency, user_company, date_from)
            for partial_line in line.matched_credit_ids:
                if partial_line.max_date <= date_from:
                    line_amount -= partial_line.company_id.currency_id._convert(partial_line.amount, user_currency, user_company, date_from)
            if not self.env.company.currency_id.is_zero(line_amount):
                undue_amounts[partner_id] += line_amount
                lines.setdefault(partner_id, [])
                lines[partner_id].append({
                    'line': line,
                    'amount': line_amount,
                    'period': qty_periods + 1,
                })

        for partner in partners:
            if partner['partner_id'] is None:
                partner['partner_id'] = False
            at_least_one_amount = False
            values = {}
            undue_amt = 0.0
            if partner['partner_id'] in undue_amounts:  # Making sure this partner actually was found by the query
                undue_amt = undue_amounts[partner['partner_id']]

            total[qty_periods+1] = total[qty_periods+1] + undue_amt
            values['direction'] = undue_amt
            if not float_is_zero(values['direction'], precision_rounding=self.env.company.currency_id.rounding):
                at_least_one_amount = True

            for i in range(qty_periods):
                during = False
                if partner['partner_id'] in history[i]:
                    during = [history[i][partner['partner_id']]]
                # Adding counter
                total[(i)] = total[(i)] + (during and during[0] or 0)
                values[str(i)] = during and during[0] or 0.0
                if not float_is_zero(values[str(i)], precision_rounding=self.env.company.currency_id.rounding):
                    at_least_one_amount = True
            values['total'] = sum([values['direction']] + [values[str(i)] for i in range(qty_periods)])
            # Add for total
            total[(i + 1)] += values['total']
            values['partner_id'] = partner['partner_id']
            if partner['partner_id']:
                values['name'] = len(partner['name']) >= 45 and partner['name'][0:40] + '...' or partner['name']
                values['trust'] = partner['trust']
            else:
                values['name'] = _('Unknown Partner')
                values['trust'] = False

            if at_least_one_amount or (self._context.get('include_nullified_amount') and lines[partner['partner_id']]):
                res.append(values)
        return res, total, lines
#