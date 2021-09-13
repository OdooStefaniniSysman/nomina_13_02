# -*- coding: utf-8 -*-
# Copyright 2019 Juan Camilo Zuluaga Serna <Github@camilozuluaga>
# Copyright 2019 Joan Marín <Github@JoanMarin>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResPartner(models.Model):
	_inherit = 'res.partner'

	tax_level_code_id = fields.Many2many('account.fiscal.position.tax.level.code', 
		'res_partner_tax_level_code_rel','res_partner_id','tax_level_code_id', 
		string='Fiscal Responsibility (TaxLevelCode)')
	tax_scheme_id = fields.Many2one(
		comodel_name='account.fiscal.position.tax.scheme',
		string='Fiscal Responsibility (TaxScheme)')
