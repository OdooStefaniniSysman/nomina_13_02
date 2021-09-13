# from odoo import api, fields, models, tools

# class ResCurrency(models.Model):
#     _inherit = 'res.currency'

#     def round(self, amount):
#         """Return ``amount`` rounded  according to ``self``'s rounding rules.

#            :param float amount: the amount to round
#            :return: rounded float
#         """
#         self.ensure_one()
#         if self._context.get('currency_rounding'):
#             return tools.float_round(amount, precision_rounding=self._context.get('currency_rounding'))
#         else:
#             return super(ResCurrency, self).round(amount)