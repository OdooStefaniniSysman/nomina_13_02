# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import Warning, UserError


class CurrencyRate(models.Model):
    _inherit = 'res.currency.rate'

    # prev_rate = fields.Float(digits=12, default=1.0)

    def write(self, vals):
        prev_rate = self.rate
        res = super(CurrencyRate, self).write(vals)
        if vals.get('rate'):
            group = self.env['res.groups'].search([('name','=','Currency Mail Notification')])
            users = group.users
            template_id = self.env.ref('currency_notification.res_currency_change_mail_template').id
            template = self.env['mail.template'].browse(template_id)
            msg_body = _('''Cordial Saludo,<br/><br/>Se ha modificado la tasa de cambio de la divisa: '''
                     '''<strong>''' + self.currency_id.name + '''</strong> <br/>'''
                     '''Tasa de cambio anterior: <strong>''' + str(prev_rate) + '''</strong><br/>'''
                     '''Nueva tasa de cambio: <strong>''' + str(self.rate) + '''</strong><br/><br/>'''
                     '''Este es un correo de caracter informativo.''')
            for user in users:
                template.subject = "Dear " + user.name
                template.email_to = user.partner_id.email or user.log
                template.body_html = msg_body
                template.send_mail(self.id, force_send=True)
        return res


    @api.onchange('rate')
    def onchange_rate(self):
        if self.ids:
            return {
                    'warning': {
                        'title': _('Advertencia cambio de TRM'),
                        'message': _('Se esta cambiando la TRM manualmente.')
                    }
            }