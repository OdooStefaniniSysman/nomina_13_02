# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import datetime, date, timedelta
from pytz import timezone


class FollowupLine(models.Model):
    _inherit = 'account_followup.followup.line'


    monday = fields.Boolean(string="Monday", default=False)
    tuesday = fields.Boolean(string="Tuesday", default=False)
    wednesday = fields.Boolean(string="Wednesday", default=False)
    thursday = fields.Boolean(string="Thursday", default=False)
    friday = fields.Boolean(string="Friday", default=False)
    monday_time = fields.Float(string="Monday time", default=8.0)
    tuesday_time = fields.Float(string="Tuesday time", default=8.0)
    wednesday_time = fields.Float(string="Wednesday time", default=8.0)
    thursday_time = fields.Float(string="Thursday time", default=8.0)
    friday_time = fields.Float(string="Friday time", default=8.0)
    monday_cron = fields.Many2one('ir.cron', string="Monday cron")
    tuesday_cron = fields.Many2one('ir.cron', string="Monday cron")
    wednesday_cron = fields.Many2one('ir.cron', string="Monday cron")
    thursday_cron = fields.Many2one('ir.cron', string="Monday cron")
    friday_cron = fields.Many2one('ir.cron', string="Monday cron")
    count_cron = fields.Integer(string='Count cron', compute='_compute_count_cron')
    account_ids = fields.Many2many(
        string='Account',
        comodel_name='account.account',
        relation='account_followup_line_rel',
        column1='account_id',
        column2='followup_line_id',
    )


    @api.depends('monday_cron','tuesday_cron','wednesday_cron','thursday_cron', 'friday_cron')
    def _compute_count_cron(self):
        for record in self:
            count = record.monday_cron and 1 or 0
            count += record.tuesday_cron and 1 or 0
            count += record.wednesday_cron and 1 or 0
            count += record.thursday_cron and 1 or 0
            count += record.friday_cron and 1 or 0
            record.count_cron = count


    def get_date_nextcall(self, num_date, time):
        date = datetime.now()
        utc_time = timezone('UTC')
        user_time = timezone(self.env.user.tz)
        diff = (user_time.localize(date) - utc_time.localize(date).astimezone(user_time)).seconds/3600
        time += diff
        hour = int(time or 0)
        minute = int((abs(time-hour) or 0) * 60)
        iso_date = datetime.isocalendar(date)

        if num_date < iso_date[2]:
            sum_day = (7 - iso_date[2]) + num_date
        elif num_date > iso_date[2]:
            sum_day = num_date - iso_date[2]
        else:
            iso_time = date.hour + (date.minute / 60)
            if time < iso_time:
                sum_day = 7
            else:
                sum_day = 0

        date_nextcall = date.replace(hour=hour, minute=minute) + timedelta(days=sum_day)
        return date_nextcall


    def cron_by_followup(self, name=False, date=False, funct=False, cron=False):
        res = False
        if cron and funct == 'unlink':
            cron.unlink()
            return True

        values = {
            'name': 'Report Followup; ' + name,
            'model_id': self.env.ref('base.model_res_partner').id,
            'user_id': self.env.ref('base.user_root').id,
            'interval_number': 1,
            'interval_type': 'weeks',
            'active': True,
            'nextcall': date,
            'numbercall': -1,
            'priority': 5,
            'doall': False,
            'state': 'code',
            'code': ''
        }

        if funct == 'create':
            res = self.env['ir.cron'].create(values)
        elif cron and funct == 'write':
            res = cron.write(values)

        return res


    def _verify_cron(self, data=False):
        if self.monday or (data and data.get('monday', False)):
            time = self.monday_time or (data and data.get('monday_time', False))
            date_nextcall = self.get_date_nextcall(1, time)
            name = (self.name or (data and data.get('name', False))) + '(monday)'
            if self.monday_cron:
                self.cron_by_followup(name=name, date=date_nextcall, funct='write', cron=self.monday_cron)
            else:
                cron = self.cron_by_followup(name=name, date=date_nextcall, funct='create')
                self.monday_cron = cron
            self.monday_cron.write({'code': 'model._cron_execute_followup(' + str(self.monday_cron.id) + ')'})

        else:
            if self.monday_cron:
                self.cron_by_followup(funct='unlink', cron=self.monday_cron)

        if self.tuesday or (data and data.get('tuesday', False)):
            time = self.tuesday_time or (data and data.get('tuesday_time', False))
            date_nextcall = self.get_date_nextcall(2, time)
            name = (self.name or (data and data.get('name', False))) + '(tuesday)'
            if self.tuesday_cron:
                self.cron_by_followup(name=name, date=date_nextcall, funct='write', cron=self.tuesday_cron)
            else:
                cron = self.cron_by_followup(name=name, date=date_nextcall, funct='create')
                self.tuesday_cron = cron
            self.tuesday_cron.write({'code': 'model._cron_execute_followup(' + str(self.tuesday_cron.id) + ')'})
        else:
            if self.tuesday_cron:
                self.cron_by_followup(funct='unlink', cron=self.tuesday_cron)

        if self.wednesday or (data and data.get('wednesday', False)):
            time = self.wednesday_time or (data and data.get('wednesday_time', False))
            date_nextcall = self.get_date_nextcall(3, time)
            name = (self.name or (data and data.get('name', False))) + '(wednesday)'
            if self.wednesday_cron:
                self.cron_by_followup(name=name, date=date_nextcall, funct='write', cron=self.wednesday_cron)
            else:
                cron = self.cron_by_followup(name=name, date=date_nextcall, funct='create')
                self.wednesday_cron = cron
            self.wednesday_cron.write({'code': 'model._cron_execute_followup(' + str(self.wednesday_cron.id) + ')'})
        else:
            if self.wednesday_cron:
                self.cron_by_followup(funct='unlink', cron=self.wednesday_cron)

        if self.thursday or (data and data.get('thursday', False)):
            time = self.thursday_time or (data and data.get('thursday_time', False))
            date_nextcall = self.get_date_nextcall(4, time)
            name = (self.name or (data and data.get('name', False))) + '(thursday)'
            if self.thursday_cron:
                self.cron_by_followup(name=name, date=date_nextcall, funct='write', cron=self.thursday_cron)
            else:
                cron = self.cron_by_followup(name=name, date=date_nextcall, funct='create')
                self.thursday_cron = cron
            self.thursday_cron.write({'code': 'model._cron_execute_followup(' + str(self.thursday_cron.id) + ')'})
        else:
            if self.thursday_cron:
                self.cron_by_followup(funct='unlink', cron=self.thursday_cron)

        if self.friday or (data and data.get('friday', False)):
            time = self.friday_time or (data and data.get('friday_time', False))
            date_nextcall = self.get_date_nextcall(5, time)
            name = (self.name or (data and data.get('name', False))) + '(friday)'
            if self.friday_cron:
                self.cron_by_followup(name=name, date=date_nextcall, funct='write', cron=self.friday_cron)
            else:
                cron = self.cron_by_followup(name=name, date=date_nextcall, funct='create')
                self.friday_cron = cron
            self.friday_cron.write({'code': 'model._cron_execute_followup(' + str(self.friday_cron.id) + ')'})
        else:
            if self.friday_cron:
                self.cron_by_followup(funct='unlink', cron=self.friday_cron)



    def write(self, values):
        result = super(FollowupLine, self).write(values)
        self._verify_cron()
        return result


    @api.model
    def create(self, values):
        result = super(FollowupLine, self).create(values)
        self._verify_cron(values)
        return result


class FollowupStatus(models.Model):
    _name = "followup.status"
    _description = "Followup status"


    name = fields.Char(string='Name')
    code = fields.Char(string='Code')

#