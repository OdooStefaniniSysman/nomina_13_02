
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
    _name = "res.users.service"
    _usage = "users"
    _collection = "base.rest.thomasgregandsons.private.services"
    _description = """
        User Services
        Access to the partner services is only allowed to authenticated users.
        If you are not authenticated go to <a href='/web/login'>Login</a>
    """
    
    def get(self, _id):
        """
        Get User's informations
        """
        user = self.env["res.users"].browse(_id)
        return self._to_json(user)

    def search(self, name):
        """
        Searh user by name
        """
        
        users = self.env["res.users"].name_search(name)
        users = self.env["res.users"].browse([i[0] for i in users])
        rows = []
        res = {"count": len(users), "rows": rows}
        for user in users:
            rows.append(self._to_json(user))
        return res


    def _get(self, _id):
        return self.env["res.users"].browse(_id)

    def _get_document(self, _id):
        return self.env["user.users"].browse(_id)

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

    def _to_json(self, user):
        res = {
            "id" : user.id,
            "name": user.name,
        }
        return res
