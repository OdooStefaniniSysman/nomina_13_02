
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
    _name = "mrp.workcenter.service"
    _usage = "CodigosCentroTrabajo"
    _collection = "base.rest.thomasgregandsons.private.services"
    _description = """
        Mrp Workcenter Services
        Access to the partner services is only allowed to authenticated users.
        If you are not authenticated go to <a href='/web/login'>Login</a>
    """
    
    def get(self, _id):
        """
        Get Mrp Workcenter's informations
        """
        workcenter = self.env["mrp.workcenter"].browse(_id)
        return self._to_json(workcenter)

    def search(self, name):
        """
        Searh Mrp Workcenter by name
        """
        
        workcenters = self.env["mrp.workcenter"].name_search(name)
        workcenters = self.env["mrp.workcenter"].browse([i[0] for i in workcenters])
        rows = []
        res = {"count": len(workcenters), "rows": rows}
        for workcenter in workcenters:
            rows.append(self._to_json(workcenter))
        return res


    def _get(self, _id):
        return self.env["mrp.workcenter"].browse(_id)

    def _get_document(self, _id):
        return self.env["mrp.workcenter"].browse(_id)

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

    def _to_json(self, workcenter):
        res = {
            "id" : workcenter.id,
            "name": workcenter.name,
        }
        return res
