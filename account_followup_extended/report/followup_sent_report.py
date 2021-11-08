# -*- coding: utf-8 -*-

from odoo import tools
from odoo import api, fields, models, _


class FollowupSentReport(models.Model):
    _name = "followup.sent.report"
    _auto = False
    _description = "Followup Sent Report"


    id = fields.Integer('ID')
    mail_id = fields.Many2one('mail.mail', 'Mail', readonly = True)
    message_id = fields.Many2one('mail.message', 'Message', readonly = True)
    partner_id = fields.Many2one('res.partner', 'Partner', readonly = True)
    author_id = fields.Many2one('res.partner', 'Author', readonly = True)
    date = fields.Datetime('Date', readonly = True)
    subject = fields.Char('Subject', readonly = True)
    message_status = fields.Char('State', readonly = True)
    qty = fields.Integer(string='Quantity', readonly=True)


    def _select(self):
        select_str = """
            mm.id AS id,
            mm.id AS mail_id,
            mme.id AS message_id,
            rp.id AS partner_id,
            ru.id AS author_id,
            mme.date AS date,
            mme.subject AS subject,
            mm.state AS message_status,
            1 AS qty
        """
        return select_str


    def _from(self):
        from_str = """
            mail_mail mm
            INNER JOIN mail_message mme ON (mme.id = mm.mail_message_id)
            INNER JOIN res_partner rp ON (rp.id = mme.res_id)
            INNER JOIN res_partner ru ON (ru.id = mme.author_id)
        """
        return from_str


    def _where(self):
        where_str = """
            mme.model = 'res.partner'
            AND mme.message_type = 'notification'
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