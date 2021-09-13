
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
    _name = "stock.production.service"
    _usage = "LotesyNumerosdeSerie"
    _collection = "base.rest.thomasgregandsons.private.services"
    _description = """
        serial Services
        Access to the partner services is only allowed to authenticated serials.
        If you are not authenticated go to <a href='/web/login'>Login</a>
    """
    
    def get(self, _id):
        """
        Get Lots informations
        """
        serial = self.env["stock.production.lot"].browse(_id)
        return self._to_json(serial)

    def search(self, name):
        """
        Searh sproduct by name
        """
        
        serials = self.env["stock.production.lot"].name_search(name)
        serials = self.env["stock.production.lot"].browse([i[0] for i in serials])
        rows = []
        res = {"count": len(serials), "rows": rows}
        for serial in serials:
            rows.append(self._to_json(serial))
        return res


    def _get(self, _id):
        return self.env["stock.production.lot"].browse(_id)

    def _get_document(self, _id):
        return self.env["stock.production.lot"].browse(_id)

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
            "product_id": {"type": "integer", "required": True, "empty": False},
            "product_name": {"type": "string", "required": False, "empty": False},

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

    def _to_json(self, serial):
        res = {
            "id" : serial.id,
            "name": serial.name,
            "product_id": serial.product_id.id,
            "product_name": serial.product_id.name
        }
        return res
