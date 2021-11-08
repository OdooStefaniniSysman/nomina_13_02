# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime,date,timedelta


class ResPartner(models.Model):
    _inherit = 'res.partner'

    send_followup = fields.Boolean(string="Send follow-up report?", default=False)
    payment_tracking = fields.Boolean(string="Payment tracking", default=False)
    type = fields.Selection(selection_add=[('portfolio', 'Portfolio tracking')])
    portfolio_contact = fields.Boolean(string='Portfolio contact', compute='_compute_portfolio_contact', store=True)
    followup_status_id = fields.Many2one('followup.status', string='Follow-up status', ondelete='restrict')
    followup_date = fields.Selection(selection=[('date', 'Create date'), ('due', 'Due date')], string='Followup date', default='due')


    @api.depends('child_ids', 'child_ids.type')
    def _compute_portfolio_contact(self):
        for record in self:
            contact = False
            if not record.parent_id and len(record.child_ids.filtered(lambda r: r.type == 'portfolio')) > 0:
                contact = True

            record.portfolio_contact = contact


    def _cron_execute_followup(self, cron=False):
        if cron:
            followup_data = self._query_followup_level(all_partners=True)
            in_need_of_action = self.env['res.partner'].browse([d['partner_id'] for d in followup_data.values() if d['followup_status'] == 'in_need_of_action'])
            in_need_of_action = in_need_of_action.filtered(lambda p: p.send_followup)
            in_need_of_action_auto = in_need_of_action.filtered(lambda p: \
                p.followup_level.auto_execute \
                and (
                    p.followup_level.monday_cron.id == cron
                    or p.followup_level.tuesday_cron.id == cron
                    or p.followup_level.wednesday_cron.id == cron
                    or p.followup_level.thursday_cron.id == cron
                    or p.followup_level.friday_cron.id == cron
                    )
                )
            in_need_of_action_auto.execute_followup()


    def _query_followup_level(self, all_partners=False):
        sql = """
            WITH unreconciled_aml AS (
                SELECT aml.id, aml.partner_id, aml.followup_line_id, aml.date, aml.date_maturity FROM account_move_line aml
                JOIN account_account account ON account.id = aml.account_id
                                            AND account.deprecated = False
                                            AND account.internal_type = 'receivable'
                JOIN account_move move ON move.id = aml.move_id
                                    AND move.state = 'posted'
                WHERE aml.reconciled = False
                AND aml.company_id = %(company_id)s
                {where}
            )
            SELECT partner.id as partner_id,
                current_followup_level.id as followup_level,
                CASE WHEN in_need_of_action_aml.id IS NOT NULL AND (prop_date.value_datetime IS NULL OR prop_date.value_datetime::date <= CURRENT_DATE) THEN 'in_need_of_action'
                        WHEN exceeded_unreconciled_aml.id IS NOT NULL THEN 'with_overdue_invoices'
                        ELSE 'no_action_needed' END as followup_status
            FROM res_partner partner
            -- Get the followup level
            LEFT OUTER JOIN account_followup_followup_line current_followup_level ON current_followup_level.id = (
                SELECT COALESCE(next_ful.id, ful.id) FROM unreconciled_aml aml
                LEFT OUTER JOIN account_followup_followup_line ful ON ful.id = aml.followup_line_id
                LEFT OUTER JOIN account_followup_followup_line next_ful ON next_ful.id = (
                    SELECT next_ful.id FROM account_followup_followup_line next_ful
                    WHERE next_ful.delay > COALESCE(ful.delay, 0)
                    AND (
                        CASE
                            WHEN partner.followup_date = 'date' THEN aml.date
                            ELSE COALESCE(aml.date_maturity, aml.date)
                            END
                        ) + next_ful.delay <= CURRENT_DATE
                    AND next_ful.company_id = %(company_id)s
                    ORDER BY next_ful.delay ASC
                    LIMIT 1
                )
                WHERE aml.partner_id = partner.id
                ORDER BY COALESCE(next_ful.delay, ful.delay, 0) DESC
                LIMIT 1
            )
            -- Get the followup status data
            LEFT OUTER JOIN account_move_line in_need_of_action_aml ON in_need_of_action_aml.id = (
                SELECT aml.id FROM unreconciled_aml aml
                LEFT OUTER JOIN account_followup_followup_line ful ON ful.id = aml.followup_line_id
                WHERE aml.partner_id = partner.id
                AND COALESCE(ful.delay, 0) < current_followup_level.delay
                AND  (
                        CASE
                            WHEN partner.followup_date = 'date' THEN aml.date
                            ELSE COALESCE(aml.date_maturity, aml.date)
                            END
                        ) + COALESCE(ful.delay, 0) <= CURRENT_DATE
                LIMIT 1
            )
            LEFT OUTER JOIN account_move_line exceeded_unreconciled_aml ON exceeded_unreconciled_aml.id = (
                SELECT aml.id FROM unreconciled_aml aml
                WHERE aml.partner_id = partner.id
                AND  (
                        CASE
                            WHEN partner.followup_date = 'date' THEN aml.date
                            ELSE COALESCE(aml.date_maturity, aml.date)
                            END
                        ) <= CURRENT_DATE
                LIMIT 1
            )
            LEFT OUTER JOIN ir_property prop_date ON prop_date.res_id = CONCAT('res.partner,', partner.id) AND prop_date.name = 'payment_next_action_date'
            WHERE partner.id in (SELECT DISTINCT partner_id FROM unreconciled_aml)
        """.format(
            where="" if all_partners else "AND aml.partner_id in %(partner_ids)s",
        )
        params = {
            'company_id': self.env.company.id,
            'partner_ids': tuple(self.ids),
        }
        self.env['account.move.line'].flush()
        self.env['res.partner'].flush()
        self.env['account_followup.followup.line'].flush()
        self.env.cr.execute(sql, params)
        result = self.env.cr.dictfetchall()
        result = {r['partner_id']: r for r in result}
        return result

#