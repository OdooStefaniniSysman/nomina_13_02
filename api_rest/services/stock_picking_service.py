# Copyright 2018 ACSONE SA/NV
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
from odoo.addons.base_rest.components.service import to_bool, to_int
from odoo.addons.component.core import Component
from odoo import api, fields, models, _
import datetime
import logging
import json

_logger = logging.getLogger(__name__)

class StockPickingService(Component):
    _inherit = "base.rest.service"
    _name = "stock.picking.service"
    _usage = "stock.picking"
    _collection = "base.rest.livingston.test.private.services"
    _description = """
        Partner Services
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
        Searh invoice by name
        """
        stock_picking_id = self.env["stock.picking"].name_search(name)
        stock_picking_id = self.env["stock.picking"].browse([i[0] for i in  stock_picking_id])
        rows = []
        res = {"count": len(stock_picking_id), "rows": rows}
        for stock_picking in stock_picking_id:
            _logger.error('*********************************\n**********************')
            _logger.error(stock_picking.id)
            rows.append(self._to_json(stock_picking))
        return res
    
    def create(self, **params):
        """
        Create a new invoice
        """
        lines = []
        lines_ids = params.pop('order_line')
        product = []
        for line in lines_ids:
            values = {'product_id':line['id'],
                      'product_qty':line['product_qty'],
                      'price_list' :line['price_list']
                       }
        
            self.env["product.product"].search(values)
        stock_picking_id = self.env["stock_picking.order"].create(self._prepare_params(params))
        return self._to_json(stock_picking)

    def update(self, _id, **params):
        """
        Update invoice informations
        """
        stock_picking_id = self._get(_id)
        stock_picking_id.write(self._prepare_params(params))
        return self._to_json(stock_picking)


    

    # The following method are 'private' and should be never never NEVER call
    # from the controller.

    def _get(self, _id):
        return self.env["stock.picking"].browse(_id)

    def _get_document(self, _id):
        return self.env["stock.picking"].browse(_id)
    #"country", "state"

    def _prepare_params(self, params):
        for key in ['partner']:
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
            #"date_order" : {"type": "datetime", "required": True, "empty": False},
            "partner_id" : {"type": "integer", "required": True, "empty": False},
            "state": {"type": "string", "required": True, "empty": False},
            "order_line" : {
                "type": "list",
                   "schema": {
                    "type": "dict",
                       "schema": {
                            "product_id" : {"type": "integer", "required": True, "empty": False},
                            "product_qty": {"type": "float", "required": True, "empty": False},
                            "price_unit" : {"type": "float", "required": False, "empty": True},
                       },
                },
            },
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

    def _to_json(self, stock_picking):
        res = {
            #"id" : stock_picking.id,
            "name": stock_picking.name,
            #"date_order" : stock_picking.date_order,
            "partner_id" : stock_picking.partner_id.id,
            "state" : stock_picking.state,
            
        }

        """"if stock_picking.order_line:
            res['order_line'] = {
                "product_id" : stock_picking.order_line.product_id.id,
                "product_qty" : stock_picking.order_line.product_qty,
                "price_unit" : stock_picking.order_line.price_unit,
            }"""

        """if product.categ_id:
            res['categ'] = {
                "id": product.categ_id.id,
                "name": product.categ_id.name,
            }"""

        
        return res