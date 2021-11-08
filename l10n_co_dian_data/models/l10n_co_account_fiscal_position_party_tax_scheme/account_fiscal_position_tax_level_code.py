# -*- coding: utf-8 -*-
# Copyright 2019 Juan Camilo Zuluaga Serna <Github@camilozuluaga>
# Copyright 2019 Joan Marín <Github@JoanMarin>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models, api


class AccountFiscalPositionTaxLevelCode(models.Model):
	_name = 'account.fiscal.position.tax.level.code'
	_description = 'Fiscal Responsibilities'
	
	name = fields.Char(string='Name')
	code = fields.Char(string='Code')

	def name_get(self):
		res = []
		for record in self:
			name = u'[%s] %s' % (record.code, record.name)
			res.append((record.id, name))    
		return res

	@api.model
	def name_search(self, name, args = None, operator = 'ilike', limit=False):
		if not args:
			args = []
		if name:
			isic = self.search(['|',
							   ('name', operator, name),
							   ('code', operator, name)] + args, limit=limit)
		else:
			isic = self.search(args, limit=limit)
		return isic.name_get()
