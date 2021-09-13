# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class AccountAnaltyticAccountnherit(models.Model):
    _inherit = 'account.analytic.account'
   
    def _compute_num_productions(self):
        production = self.env["mrp.production"]
        for analytic_account in self:
            domain = [("analytic_account_id", "=", analytic_account.id)]
            analytic_account.num_productions = production.search_count(domain)

    department_id = fields.Many2one("hr.department", "Department")
    num_productions = fields.Integer(compute="_compute_num_productions")

    @api.model
    def create(self, vals):
        if 'code' in vals:
            if vals['code']:
                leads = self.env['account.analytic.account'].search([('code', '=', vals['code'])])
                if leads:
                    raise ValidationError("Ya existe esta referencia")
        res = super(AccountAnaltyticAccountnherit, self).create(vals)
        return res

    def unlink(self):
        for record in self:
            if record.debit != 0 or record.credit != 0:
                raise ValidationError("No se puede eliminar una cuenta con movimientos")
            return super(AccountAnaltyticAccountnherit, self).unlink()


class AccountAnaltyticGroupInherit(models.Model):
    _inherit = 'account.analytic.group'

    @api.model
    def create(self, vals):
        if 'description' in vals:
            if vals['description']:
                leads = self.env['account.analytic.group'].search([('description', '=', vals['description'])])
                if leads:
                    raise ValidationError("Ya existe esta descripción")
        res = super(AccountAnaltyticGroupInherit, self).create(vals)
        return res


class AnalyticLine(models.Model):
    _inherit = "account.analytic.line"

    @api.model
    def _default_department(self):
        department_id = False
        employee = self.env.user.employee_ids
        if employee and employee[0].department_id:
            department_id = employee[0].department_id.id
        return department_id

    department_id = fields.Many2one(
        "hr.department",
        "Department",
        default=lambda self: self._default_department(),
        help="User's related department",
    )
    account_department_id = fields.Many2one(
        comodel_name="hr.department",
        related="account_id.department_id",
        string="Account Department",
        store=True,
        readonly=True,
        help="Account's related department",
    )
