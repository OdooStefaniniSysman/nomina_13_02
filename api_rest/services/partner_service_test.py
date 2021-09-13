# Copyright 2018 ACSONE SA/NV
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
from odoo.addons.base_rest.components.service import to_bool, to_int
from odoo.addons.component.core import Component
from odoo import api, fields, models, SUPERUSER_ID, _
import datetime
import logging
import json

_logger = logging.getLogger(__name__)


class InvoiceService(Component):
    _inherit = "base.rest.service"
    _name = "partner.service.test"
    _usage = "test"
    _collection = "base.rest.livingston.test.private.services"
    _description = """
        Invoice Services
        Access to the partner services is only allowed to authenticated users.
        If you are not authenticated go to <a href='/web/login'>Login</a>
    """
    
    def get(self, _id):
        """
        Get invoice's informations
        """
        return self._to_json(self._get(_id))

    def search(self, name):
        """
        Searh invoice by ref
        """
        
        invoices = self.env["account.move"].name_search(name)
        invoices = self.env["account.move"].browse([i[0] for i in invoices])
        rows = []
        res = {"count": len(invoices), "rows": rows}
        for invoice in invoices:
            rows.append(self._to_json(invoice))
        return res
    """
    def _prepare_invoice(self):
        #self.ensure_one()
        invoice_vals = {
            "ref1_comfiar": "jdfduy",
            'ref': 'cualquie cosa',
            'type': 'out_invoice',
            'narration': 'narration note',
            'currency_id': 8,
            'campaign_id': '',
            'medium_id': '',
            'source_id': '',
            #'invoice_user_id': self.user_id and self.user_id.id,
            #'team_id': self.team_id.id,
            'partner_id': 30,
            'partner_shipping_id': 30,
            #'invoice_partner_bank_id': self.company_id.partner_id.bank_ids[:1].id,
            #'fiscal_position_id': self.fiscal_position_id.id or self.partner_invoice_id.property_account_position_id.id,
            'journal_id': 3,  # company comes from the journal
            'invoice_origin': 'dsfsdfsdfsd',
            'invoice_payment_term_id': 1,
            'invoice_payment_ref': 'sdfsdfsdfsdf',
            #'transaction_ids': [(6, 0, self.transaction_ids.ids)],
            'invoice_line_ids': [],
            'company_id': 1
        }
        return invoice_vals
        
    def _prepare_invoice_line(self):
        #self.ensure_one()
        res = {
            'display_type': '',
            'sequence': 11,
            'name': 'nombre',
            'product_id': 2227,
            #'product_uom_id': self.product_uom.id,
            'quantity': 12,
            'discount': 0,
            'price_unit': 100000,
            'tax_ids': [(6, 0, [9])],
            #'analytic_account_id': self.order_id.analytic_account_id.id,
            #'analytic_tag_ids': [(6, 0, self.analytic_tag_ids.ids)],
            #'sale_line_ids': [(4, self.id)],
        }
        return res
    """
    
    def create(self, **params):
        """
        Create a new invoice
        """
        #precision = self.env['decimal.precision'].precision_get('Product Unit of Measure')
        #invoice_vals_list = []   
        #invoice_line_ids = params.pop('invoice_line_ids')
        #invoice_vals = params
        #_logger.error(invoice_line_ids[0])
        #invocie_lines_2 = []
        #invoice_lines_2A = [invocie_lines_2.append(((0, 0, line))) for line in invoice_line_ids]      
        #invoice_vals['invoice_line_ids'] = invoice_lines_2A
        #_logger.error(invoice_vals)
        #invoice_vals_list.append(invoice_vals)
        invoice_vals_list = []
        invoice_line_ids = params.pop('invoice_line_ids')
        invoice_vals = params
        _logger.error(invoice_line_ids[0])
        invoice_lines = []
        for line in invoice_line_ids:
            a = ((0, 0, line))
            invoice_lines.append(a)
        invoice_vals['invoice_line_ids'] = invoice_lines
        _logger.error(invoice_vals)
        #.with_context(default_type='out_invoice')
        invoice_vals_list.append(invoice_vals)
        moves = self.env['account.move'].sudo().create(invoice_vals_list)
        return self._to_json(moves)

    def update(self, _id, **params):
        """
        Update invoice informations
        """
        invoice = self._get(_id)
        invoice.write(self._prepare_params(params))
        return self._to_json(invoice)

   

    # The following method are 'private' and should be never never NEVER call
    # from the controller.

    def _get(self, _id):
        return self.env["account.move"].browse(_id)

    def _get_document(self, _id):
        return self.env["account.move"].browse(_id)
    #"country", "state"

    def _prepare_params(self, params):
        for key in ["partner","invoice_payment_term","payment_mean","journal", "currency", "product"]:
            if key in params:
                val = params.pop(key)
                if val.get("id"):
                    params["%s_id" % key] = val["id"]
        return params



    # Validator
    def _validator_return_get(self):
        res = self._validator_create()
        res.update({"id": {"type": "integer", "required": True, "empty": False}})
        return res

    def _validator_search(self):
        return {"name": {"type": "string", "nullable": False, "required": True}}
    

        
    def _validator_return_search(self):
        return {
            "count": {"type": "integer", "required": True},
            "rows": {
                "type": "list",
                "required": True,
                "schema": {"type": "dict", "schema": self._validator_return_get()},
            },
        }
    


    def _validator_create(self):
        res = {
            #"id" : {"type": "integer", "required": True, "empty": False}, 
            "name": {"type": "string", "required": True, "empty": False},
            "partner_id" : {"type": "integer", "required": True, "empty": False}, 
            "ref1_comfiar": {"type": "string"},
            "invoice_origin" : {"type": "string", "required": True, "empty": False},
            #"invoice_date" : {"type": "date",  "required": True, "empty": False},
            "type" :  {"type": "string", "required": True, "empty": False},
            "send_invoice_to_dian" :{"type": "string", "required": True, "empty": False},
            "operation_type": {"type": "string", "required": True, "empty": False},
            "invoice_type_code" : {"type": "string", "required": True, "empty": False},
            "invoice_payment_term_id": {"type": "integer", "required": True, "empty": False},
            "payment_mean_id":  {"type": "integer", "required": True, "empty": False}, 
            "journal_id":  {"type": "integer", "required": True, "empty": False}, 
            "currency_id":  {"type": "integer", "required": True, "empty": False}, 


            "invoice_line_ids" : {
                "type": "list",
                "schema":{
                    "type" : "dict",
                    "schema":{
                    #"product_id" :{"type": "integer", "coerce": to_int, "nullable": True},
                    #"id": {"type": "integer", "coerce": to_int, "nullable": True},
                    "product_id" : {"type": "integer", "required": True, "empty": False},
                    "name": {"type": "string", "required": True, "empty": False},
                    "ref_comfiar": {"type": "string", "required": True, "empty": False},
                    "muestra_ref" : {"type": "string", "required": True, "empty": False},
                    "lote_ref" : {"type": "string", "required": True, "empty": False},
                    "informe_ref" : {"type": "string", "required": True, "empty": False},
                    "cotizacion_ref" : {"type": "string", "required": True, "empty": False},
                    "product_ref" :  {"type": "string", "required": True, "empty": False},
                    "account_id" :  {"type": "integer", "coerce": to_int, "nullable": True},
                    "price_unit" :  {"type": "float", "required": True, "empty": False},
                    "discount" : {"type": "float", "required": True, "empty": False},
                    "tax_ids" : {
                        "type" : "list",   
                    }   
                },
            },
            },
            "state": {"type": "string", "required": True, "empty": False},
            

        }
        return res

    def _validator_return_create(self):
        return self._validator_return_get()

    def _validator_update(self):
        res = self._validator_create()
        for key in res:
            if "required" in res[key]:
                del res[key]["required"]
        return res

    def _validator_return_update(self):
        return self._validator_return_get()

    def _validator_archive(self):
        return {}

    def _to_json(self, invoice):
        
        _logger.error('*********************************\n**********************')
        _logger.error(invoice.id)
        _logger.error(invoice.name)
        
        
        res = {
            "id" : invoice.id,
            "name": invoice.name,
            #"ref1_comfiar" : invoice.ref1_comfiar,
            "invoice_origin" : invoice.invoice_origin,
            "invoice_date" : invoice.invoice_date,
            "type" : invoice.type,
            "send_invoice_to_dian" : invoice.send_invoice_to_dian,
            "operation_type" : invoice.operation_type,
            "invoice_type_code" : invoice.invoice_type_code,
            "state": invoice.state,
            "partner_id": invoice.partner_id.id,
            "invoice_payment_term_id": invoice.invoice_payment_term_id.id,
            "payment_mean_id": invoice.payment_mean_id.id,
            "journal_id": invoice.journal_id.id,
            "currency_id": invoice.currency_id.id,
            #"discount": invoice.discount,
            #"price_unit": invoice.price_unit,
            
            
            #"ref" : invoice.ref,             
        }
        """
        dic = []
        for line in invoice.invoice_line_ids:
            dic += [({
                "display_type": line.display_type,
                "sequence": line.sequence,
                "name": line.name,
                "product_id": line.product_id.id,
                "quantity": line.quantity,
                "discount": line.discount,
                "price_unit": line.price_unit,
                "cotizacion_ref": line.cotizacion_ref if line.cotizacion_ref else '',
                "lote_ref": line.lote_ref if line.lote_ref else '',
                "informe_ref": line.informe_ref if line.informe_ref else '',
                "muestra_ref": line.muestra_ref if line.muestra_ref else '',
                "project_ref": line.project_ref,
                "ref_comfiar": line.ref_comfiar,
                "product_ref": line.product_ref
            })]
        res.update({'invoice_line_ids': dic})
        
        _logger.error(dic)
        """
        #res = json.dumps(res)

        return res   