# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import datetime, timedelta
from odoo.exceptions import UserError, ValidationError
import logging

_logger = logging.getLogger(__name__)


class AccountPaymentMultiReconcile(models.TransientModel):
	_name="account.payment.multi.reconcile"

	memo = fields.Char(string='Observaciones')
	journal_id = fields.Many2one('account.journal',string='Diario de Conciliación',domain=[('type', '=', 'bank')],required=True)
	journal_payment_id = fields.Many2one('account.journal',string='Diario de Pago',domain=[('type', '=', 'bank')],required=True, readonly=True)
	payment_ids = fields.One2many(
		comodel_name='account.payment.multi.reconcile.payment',
		inverse_name='reconcile_id',
		string='Ingresos Afectados',
		readonly=True,
		required=True,
	)
	currency_id = fields.Many2one('res.currency', string="Moneda de la Compañia", related='journal_id.company_id.currency_id', readonly=True)
	partner_id = fields.Many2one('res.partner',string='Tercero', related='journal_id.partner_id', readonly=True,required=True)
	amount_base = fields.Monetary(string='Base para impuestos')
	date = fields.Date('Fecha de Conciliación',required=True, default=datetime.today())
	tax_ids = fields.One2many(
		comodel_name='account.payment.multi.reconcile.tax',
		inverse_name='reconcile_id',
		string='Impuestos',
	)
	bank_base_tax_amount = fields.Float(string='% Impuesto del IVA',related='journal_id.bank_base_tax_id.amount')
	account_analytic_tag_id = fields.Many2one('account.analytic.tag',string='Etiqueta Analítica', readonly=True)

	def _compute_amount_base_payment(self):
		self.amount_base = 0.0
		payment_data = self.env['account.payment'].search([('id','ind',self.payment_ids),('state','=','posted')])
		for payment in payment_data:
			self.amount_base += payment.amount
		
	def _get_payments(self):
		return self.env['account.payment'].browse(self._context.get('active_ids',[]))

	@api.onchange('journal_id')
	def _onchange_journal_id(self):
		if not self.journal_id.partner_id and self.journal_id:
			raise UserError(_("El diario seleccionado debe tener un tercero asociado"))

		self.amount_base = 0.0
		for payment in self.payment_ids:
			self.amount_base += payment.amount


		self.amount_base = self.amount_base / (1+(self.bank_base_tax_amount/100))

		#remove list after refill
		for tax in self.tax_ids:
			self.write({'tax_ids': [( 2, tax.id)]})

		tax_list = []
		rec = {}
		commission_ok = 0
		for tax in self.journal_id.bank_tax_ids:
			amount = tax.amount
			if tax.commission_tax_ok:
				for commission in self.journal_id.bank_commission_ids:
					if commission.journal_payment_method_id.id == self.journal_payment_id.id:
						amount = commission.amount_percent
				# un impuesto de gasto bancarios desde el metodo de pago se usa para calcular el impuesto sobre la comisión
				if self.journal_payment_id.bank_base_tax_id:
					self.write({'tax_ids': [( 0,0, {
						'tax_id': self.journal_payment_id.bank_base_tax_id.id,
						'amount': (self.amount_base * amount / 100) * (self.journal_payment_id.bank_base_tax_id.amount / 100),
					})]})
			self.write({'tax_ids': [( 0,0, {
				'tax_id': tax.id,
				'amount': 0,
			})]})

		
		return rec

	@api.model
	def default_get(self, fields):
		context = dict(self._context or {})
		active_model = context.get('active_model')
		active_ids = context.get('active_ids')
		payments = self.env[active_model].browse(active_ids)
	
		if any(payment.state != 'posted' for payment in payments):
			raise UserError(_("Solo puede conciliar ingresos en estado validado"))

		if any(payment.validate_treasury_ok == True for payment in payments):
			raise UserError(_("Solo puede conciliar ingresos que no hayan sido conciliados anteriormente"))

		if any(payment.journal_id.type != 'bank' for payment in payments):
			raise UserError(_("Solo puede conciliar ingresos de banco y en este caso está incluyendo ingresos en efectivo"))

		#if any(MAP_INVOICE_TYPE_PARTNER_TYPE[inv.type] != MAP_INVOICE_TYPE_PARTNER_TYPE[invoices[0].type]
		#		   for inv in invoices):
		#		raise UserError(_("No se puede mezclar facturas de cliente y proveedor"
		#					  " en un mismo documento de pago"))
			
		if any(pay.currency_id != payments[0].currency_id for pay in payments):
			raise UserError(_("Para conciliar multiples ingresos a la vez, estos deben tener la misma moneda."))

		rec = {}
		payment_list = []
		total_amount = 0
		journal_cont = 0
		journal_payment_id = None
		account_analytic_tag_id = None
		for pay in payments:
			if journal_payment_id != pay.journal_id.id and journal_payment_id:
				journal_payment_id = pay.journal_id.id
				journal_cont+=1
			if not journal_payment_id:
				journal_payment_id = pay.journal_id.id
			total_amount += pay.amount
			payment_list.append((0,0,{
				'payment_id' : pay.id,
				'amount' : pay.amount,
				'journal_id' : pay.journal_id.id,
				'payment_date' : pay.payment_date,
				'payment_account_id' : pay.journal_id.default_credit_account_id.id,
				'partner_id': pay.partner_id.id,
				'name': pay.name,
				}))
			if not pay.session_id.config_id.account_analytic_tag_id.id:
				raise UserError(_("El punto de venta asociado a este método de pago no tiene definido una cuenta analítica."))
			else:
				account_analytic_tag_id = pay.session_id.config_id.account_analytic_tag_id.id

		if journal_cont > 0:
			raise UserError(_("Lo ingresos seleccionados deben ser del mismo Diario o Método de Pago"))
		rec.update({'payment_ids':payment_list})
		rec.update({
			'partner_id': self.journal_id.partner_id.id,
			'amount_base': total_amount,
			'journal_payment_id': journal_payment_id,
		})
		if account_analytic_tag_id:
			rec.update({
				'account_analytic_tag_id': account_analytic_tag_id,
			})
		return rec

	def action_view_conciliation_move(self):
		return True

	def register_multi_payment(self):

		if self.payment_ids:
			account_move = self.env['account.move']
			ctx = dict(self._context, lang=self.partner_id.lang)
			move_lines = []
			account_reconcile_id = self.journal_id.default_debit_account_id
			total_amount = 0.0
			for payment in self.payment_ids:
				total_amount += payment.amount
				account_payment_id = self.env['account.payment'].search([('id','=',payment.payment_id)]).journal_id.default_debit_account_id
				move_lines.append({
                    'name': str(payment.name),
                    'debit': 0.0, 
                    'credit': payment.amount,
                    'account_id': account_payment_id.id,
                    'date': self.date,
                    'partner_id': payment.partner_id.id,
                    'quantity': 1,
	                'amount_currency': 0.0,
                    'currency_id': False,
                    'analytic_tag_ids': [(4, self.account_analytic_tag_id.id)]
                    #'payment_id': payment.payment_id,
                })


			tax_amount = 0.0
			for tax in self.tax_ids:
				tax_amount += round(abs(tax.amount), 2)
				move_lines.append({
                    'name': str(tax.tax_id.amount) + ' %\nBase: ' + str(round(self.amount_base,2)),
                    'debit': abs(round(tax.amount, 2)), 
                    'credit': 0.0,
                    'account_id': tax.account_id.id,
                    'date': self.date,
                    'partner_id': self.partner_id.id,
                    'quantity': 1,
                	'amount_currency': 0.0,
                	'currency_id': False,
                	'analytic_tag_ids': [(4, self.account_analytic_tag_id.id)]
                })

			move_lines.append({
                'name': 'Conciliación Bancaria',
                'debit': total_amount - abs(tax_amount), 
                'credit': 0.0,
                'account_id': account_reconcile_id.id,
                'date': self.date,
                'partner_id': self.partner_id.id,
                'quantity': 1,
                'amount_currency': 0.0,
                'currency_id': False,
                'analytic_tag_ids': [(4, self.account_analytic_tag_id.id)]
            })
			move_vals = {
				'ref': 'Conciliación Bancaria: ' + str(self.memo),
                'journal_id': self.journal_id.id,
                'date': self.date,
                'name': '/',
			}

			move = self.env['account.move'].with_context(default_journal_id=move_vals['journal_id']).create(move_vals)
			move.write({'line_ids': [(0, 0, line) for line in move_lines]})
			move.post()
			for payment in self.payment_ids:
				payment_obj = self.env['account.payment'].search([('id','=',payment.payment_id)])
				moveline_ids = self.env['account.move.line'].search([('payment_id','=',payment.payment_id),('debit','!=',0),('reconciled','=',False)])
				moveline_ids += self.env['account.move.line'].search([('credit','!=',0),('reconciled','=',False),('move_id','=',move.id),('name','=',payment.name)])
				vals = []
				account_id = 0
				for line in moveline_ids:
					if account_id != line.account_id.id and account_id > 0:
						raise UserError(_("Las cuentas para conciliar deben ser iguales. Ingreso: " + str(payment.name)))
					account_id = line.account_id.id
					#self.env['account.move.line'].search([('id','=',line.id)]).write({'reconciled': True})
				moveline_ids.reconcile()
				payment_obj.write({
					'treasury_move_id': move.id,
					'validate_treasury_ok': True,
					'state': 'reconciled'
				})
		else:
			raise UserError(_("Ocurrio un error recuperando los datos de los ingresos, por favor recargue la página e intente realizar el procedimiento nuevamente."))

		return True
		

class AccountPaymentMultiReconcileTax(models.TransientModel):
    _name = 'account.payment.multi.reconcile.tax'

    reconcile_id = fields.Many2one('account.payment.multi.reconcile',string='Impuestos')
    account_id = fields.Many2one('account.account',string='Cuenta Contable', compute='_compute_account_from_tax')
    tax_id = fields.Many2one('account.tax',string='Impuesto',domain="[('type_tax_use','=','sale')]")
    amount = fields.Float(string='Valor')

    @api.depends('reconcile_id.amount_base','tax_id.amount')
    def _compute_account_from_tax(self):
    	for rec in self:
    		amount = rec.tax_id.amount
    		if rec.tax_id.id > 0:
    			account_id = self.env['account.tax.repartition.line'].search([('invoice_tax_id','=',rec.tax_id.id),('repartition_type','=','tax')]).account_id.id
    			if account_id:
    				rec.account_id = account_id
    				if rec.tax_id.commission_tax_ok:
    					for commission in self.reconcile_id.journal_id.bank_commission_ids:
    						if commission.journal_payment_method_id.id == self.reconcile_id.journal_payment_id.id:
    							amount = commission.amount_percent
    				#para evitar recalculo en el impuesto de iva sobre la comisión del metodo de pago
    				if rec.tax_id.id != self.reconcile_id.journal_payment_id.bank_base_tax_id.id:
    					#if rec.amount == 0:
    					if not rec.amount:
    						rec.amount = rec.reconcile_id.amount_base * amount / 100
    			else:
    				raise UserError(_("El impuesto seleccionado debe tener cuenta contable asociada para facturación"))
    		else:
    			rec.account_id = False


class AccountPaymentMultiReconcileLine(models.TransientModel):
    _name = 'account.payment.multi.reconcile.payment'

    reconcile_id = fields.Many2one('account.payment.multi.reconcile',string='Formulario de Concilización')
    payment_id = fields.Integer(string="ID del Ingreso")
    amount = fields.Float("Total Ingreso", required=False)
    journal_id = fields.Many2one('account.journal',string='Diario')
    payment_account_id = fields.Many2one('account.account',string='Cuenta')
    payment_date = fields.Date('Fecha')
    name = fields.Char(string='No. de Ingreso')
    partner_id = fields.Many2one('res.partner',string='Cliente')
