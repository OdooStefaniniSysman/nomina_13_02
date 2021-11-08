# -*- coding: utf-8 -*-

from odoo import tools
from odoo import api, fields, models, _


class AccountPaymentReport(models.Model):
    _name = "account.payment.report"
    _auto = False
    _description = "Account Payment Report"


    id = fields.Integer('ID')
    payment_id = fields.Many2one('account.payment', 'Payment', readonly = True)
    partner_id = fields.Many2one('res.partner', 'Partner', readonly = True)
    journal_id = fields.Many2one('account.journal', 'Journal', readonly = True)
    company_id = fields.Many2one('res.company', 'Company', readonly = True)
    currency_id = fields.Many2one('res.currency', 'Currency', readonly = True)
    move_id = fields.Many2one('account.move', 'Invoice', readonly = True)
    identification = fields.Char('Identification', readonly = True)
    payment_date = fields.Date('Payment Date', readonly = True)
    imp_mi = fields.Char('Imp MI', readonly = True)
    move_ref = fields.Char('Reference', readonly = True)
    payment_amount = fields.Float('Amount payment', readonly = True)
    debit_credit = fields.Float('D/H', readonly = True)
    tax_iva = fields.Float('Amount tax', readonly = True)
    amount_untaxed = fields.Float('Amount Subtotal', readonly = True)
    amount_total = fields.Float('Amount Total', readonly = True)
    variation = fields.Float('Variation', readonly = True)
    payment_ref = fields.Char('Payment Reference', readonly = True)


    def _select(self):
        select_str = """
            row_number() OVER() AS id,
            ap.id AS payment_id,
            rp.id AS partner_id,
            aj.id AS journal_id,
            rc.id AS company_id,
            cur.id AS currency_id,
            CASE 
                WHEN rp.identification_document IS NOT NULL THEN rp.identification_document
                WHEN rp.ref IS NOT NULL THEN rp.ref
                ELSE '-' 
            END AS identification,
            ap.payment_date AS payment_date,
            0.0 AS imp_mi,
            am.id AS move_id,
            am.ref AS move_ref,
            COALESCE(ap.amount, 0.0) AS payment_amount,
            COALESCE((SELECT sum(amount_total) FROM account_move WHERE refund_type = 'debit' and reversed_entry_id = am.id), 0.0)
            -
            COALESCE((SELECT sum(amount_total) FROM account_move WHERE refund_type = 'credit' and reversed_entry_id = am.id), 0.0)
            AS debit_credit,
            COALESCE(
                (
                SELECT
                    SUM(credit-debit)
                FROM
                    account_move_line
                WHERE
                    move_id = am.id
                    AND account_id IN (SELECT id FROM account_account WHERE code like '240805%')
                ),
            0.0) AS tax_iva,
            COALESCE(am.amount_untaxed, 0.0) AS amount_untaxed,
            COALESCE(am.amount_total, 0.0) AS amount_total,
            COALESCE(
                (
                SELECT
                    SUM(credit-debit)
                FROM
                    account_move_line
                WHERE
                    move_id = am.id
                    AND account_id IN (SELECT id FROM account_account WHERE code like '1355%')
                ),
            0.0) AS variation,
            ap.communication AS payment_ref
        """
        return select_str


    def _from(self):
        from_str = """
            account_payment ap
            INNER JOIN res_partner rp ON (rp.id = ap.partner_id)
            INNER JOIN account_journal aj ON (aj.id = ap.journal_id)
            INNER JOIN res_company rc ON (rc.id = aj.company_id)
            INNER JOIN account_invoice_payment_rel ai_rel ON (ai_rel.payment_id = ap.id)
            INNER JOIN account_move am ON (am.id = ai_rel.invoice_id)
            INNER JOIN account_move_line aml ON (aml.payment_id = ap.id AND aml.name = ap.name)
            INNER JOIN res_currency cur ON (cur.id = ap.currency_id)
        """
        return from_str


    def _where(self):
        where_str = """
            ap.state NOT IN ('draft', 'cancelled')
            AND ap.payment_type = 'inbound'
        """
        return where_str


    def init(self):
        # self._table = account_invoice_report
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute("""CREATE or REPLACE VIEW %s as (
            SELECT
                %s
            FROM
                %s
            WHERE 
                %s
        )""" % (
                self._table, self._select(), self._from(), self._where()
            ))


#