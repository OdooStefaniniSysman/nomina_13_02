# Copyright 2018 ACSONE SA/NV
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
from odoo.addons.base_rest.components.service import to_bool, to_int
from odoo.addons.component.core import Component



class ProductService(Component):
    _inherit = "base.rest.service"
    _name = "product.service"
    _usage = "product"
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
        products = self.env["product.product"].name_search(name)
        products = self.env["product.product"].browse([i[0] for i in products])
        rows = []
        res = {"count": len(products), "rows": rows}
        for product in products:
            rows.append(self._to_json(product))
        return res
    
    def create(self, **params):
        """
        Create a new invoice
        """
        product = self.env["product.product"].create(self._prepare_params(params))
        return self._to_json(product)

    def update(self, _id, **params):
        """
        Update invoice informations
        """
        product = self._get(_id)
        product.write(self._prepare_params(params))
        return self._to_json(product)


    

    # The following method are 'private' and should be never never NEVER call
    # from the controller.

    def _get(self, _id):
        return self.env["product.product"].browse(_id)

    def _get_document(self, _id):
        return self.env["product.product"].browse(_id)
    #"country", "state"

    def _prepare_params(self, params):
        for key in ['categ']:
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
            "id" : {"type": "integer", "required": True, "empty": False},
            "name": {"type": "string", "required": True, "empty": False},
            "sale_ok" : {"type": "boolean", "required": True, "empty": False},
            "default_code" : {"type": "string", "required": True, "empty": False},
            "categ" : {
                "type": "dict",
                "schema": {
                    "id": {"type": "integer", "coerce": to_int, "nullable": True},
                    "name": {"type": "string"},
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

    def _to_json(self, product):
        res = {
            "id" : product.id,
            "name": product.name,
            "sale_ok" : product.sale_ok,
            "default_code" : product.default_code,
            
        }

        if product.categ_id:
            res['categ'] = {
                "id": product.categ_id.id,
                "name": product.categ_id.name,
            }

        
        return res

        