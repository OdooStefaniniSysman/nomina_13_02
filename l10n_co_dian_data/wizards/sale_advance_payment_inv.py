from odoo import api, fields, models

class SaleAdvancePaymentInv(models.TransientModel):
    _inherit = 'sale.advance.payment.inv'

    journal_id = fields.Many2one('account.journal', string='Journal', domain=lambda self: [('type','=','sale'), ('company_id', '=', self.env.company.id)])
    grouped_sale_partner = fields.Boolean(string='Agrupar por cliente', default=False)

    def create_invoices(self):
        if not self.grouped_sale_partner:
            self = self.with_context(grouped_sale_partner=True)
        if self.journal_id:
            self = self.with_context(default_journal_id=self.journal_id.id)
        return super(SaleAdvancePaymentInv, self).create_invoices()
    
