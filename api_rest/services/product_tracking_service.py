
# Copyright 2018 ACSONE SA/NV
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
from odoo.addons.base_rest.components.service import to_bool, to_int
from odoo.addons.component.core import Component
from odoo import api, fields, models, SUPERUSER_ID, _
from datetime import datetime
import logging
import json

_logger = logging.getLogger(__name__)


class Service(Component):
    _inherit = "base.rest.service"
    _name = "product.tracking.service"
    _usage = "TrackingProduct"
    _collection = "base.rest.thomasgregandsons.private.services"
    _description = """
        product Services
        Access to the partner services is only allowed to authenticated products.
        If you are not authenticated go to <a href='/web/login'>Login</a>
    """
    
    def get(self, _id):
        """
        Get Product informations
        """
        product = self.env["product.product"].browse(_id)
        return self._to_json(product)

    def search(self, name):
        """
        Searh product by name
        """
        
        products = self.env["product.product"].name_search(name)
        products = self.env["product.product"].search([('is_tracking_papper_api','=',True)])#.browse([i[0] for i in products])
        rows = []
        res = {"count": len(products), "rows": rows}
        for product in products:
            rows.append(self._to_json(product))
        return res


    def _get(self, _id):
        return self.env["product.product"].browse(_id)

    def _get_document(self, _id):
        return self.env["product.product"].browse(_id)

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
             
            "name": {"type": "string", "required": True, "empty": False},
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

    def _to_json(self, product):
        res = {
            "id": product.id,
            "name": product.name
        }
        return res
