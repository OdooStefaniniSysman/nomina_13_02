# -*- coding: utf-8 -*-
# Copyright 2020-TODAY Miguel Pardo <ing.miguel.pardo@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from odoo import fields, models


class HrContract(models.Model):
    """Hr Contract."""

    _inherit = 'hr.contract'

    recruitment_reason_id = fields.Many2one(
        'recruitment.reason',
        'Recruitment Reasons', copy=False)
    create_absence = fields.Boolean(string='Create Absence', compute='_compute_create_absence_contract')

    def _compute_create_absence_contract(self):
        for record in self:
            if record.tipo_de_salario_contrato in ['APOYO SOSTENIMIENTO', 'apoyo_sostenimiento']:
                record.create_absence = False
            else:
                record.create_absence = True


class HrContractFlexWage(models.Model):
    _inherit = 'hr.contract.flex_wage'

    pv_id = fields.Many2one('hr.pv')
