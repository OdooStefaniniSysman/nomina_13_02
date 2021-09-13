
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
    _name = "mrp.production.service"
    _usage = "ActualizacionInsumoPapel"
    _collection = "base.rest.thomasgregandsons.private.services"
    _description = """
        Production Services
        Access to the partner services is only allowed to authenticated production.
        If you are not authenticated go to <a href='/web/login'>Login</a>
    """
    
    def get(self, _id):
        """
        Get Production informations
        """
        production = self.env["mrp.production"].browse(_id)
        return self._to_json(production)

    def search(self, name):
        """
        Searh Production by name
        """
        
        productions = self.env["mrp.production"].name_search(name)
        productions = self.env["mrp.production"].browse([i[0] for i in productions])
        rows = []
        res = {"count": len(productions), "rows": rows}
        for production in productions:
            rows.append(self._to_json(production))
        return res


    def _get(self, _id):
        return self.env["mrp.production"].browse(_id)

    def _get_document(self, _id):
        return self.env["mrp.production"].browse(_id)

    # Validator
    def _validator_return_get(self):
        res = self._validator_create()
        res.update({"id": {"type": "integer", "required": False, "empty": True}})
        return res

    def _validator_search(self):
        #return {"id": {"type": "integer", "nullable": False, "required": False}}
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
            "msg": {"type": "string", "required": False, "empty": True},
            "code": {"type": "string", "required": False, "empty": True},
            "name": {"type": "string", "required": False, "empty": True},
            "product_id": {"type": "integer", "required": False, "empty": True},
            "lot_id": {"type": "integer", "required": False, "empty": True},
            "product_name": {"type": "string", "required": False, "empty": True},
            "state": {"type": "string", "required": False, "empty": True},
            "company_id": {"type": "integer", "required": False, "empty": True},
            "company_name": {"type": "string", "required": False, "empty": True},
            #"date_planned_start": {"type": "date", "required": True, "empty": False},
            "routing_id": {"type": "integer", "required": False, "empty": True},
            "routing_name": {"type": "string", "required": False, "empty": True},

        }
        return res
    
    
    def update(self, **params):
        """
        Update production papper consumables informations
        """
        keys = ['name','product_id','lot_id']
        for key in keys:
            if key not in params:
                return {
                    'code': '041',
                    'msg': 'No están bien definidos los nombres de los campos en el json!',
                }
        if not params.get('name'):
            return {
                'code': '042',
                'msg': 'Debe enviar el número de orden de fabricación en campo name!',
            }
        if not params.get('lot_id'):
            return {
                'code': '043',
                'msg': 'Debe enviar el lote/N.serie de papel para orden de fabricación en campo lot_id!',
            }
        if not params.get('product_id'):
            return {
                'code': '044',
                'msg': 'Debe enviar el código del producto papel para orden de fabricación en campo product_id!',
            }
        
        
        _logger.error(params)
        production_id = self.env['mrp.production'].search([('name','=',params.get('name'))])
        _logger.error('****************************\jn+++++++++++++++++')
        _logger.error(production_id)
        if production_id.state == 'progress':
            _logger.error(production_id.state)
            for move in production_id.move_raw_ids:
                _logger.error(move.product_id.is_tracking_papper_api)
                _logger.error(params.get('product_id'))
                _logger.error(params.get('lot_id'))
                if move.product_id.is_tracking_papper_api and move.product_id.id == params.get('product_id'):
                    _logger.error('Entrando con producto valido')
                    for moveline in move.move_line_ids:
                        _logger.error(moveline)
                        try:
                            #self.env.cr.execute("""UPDATE stock_move_line set lot_id = 10 where id = 47""")
                            
                            moveline.sudo().write({
                                'lot_id': params.get('lot_id'),
                            })
                            _logger.error('+++++++++++++++++++++++++++++++++++++++lot_id')
                            _logger.error(params.get('lot_id'))
                        except Exception as e:
                            _logger.error(e)
                        _logger.error('Actualizado con exito')
                        return {
                            'code': '021',
                            'msg': 'Orden de Fabricación actualizada con exito!',
                        }
                else:
                    return {
                            'code': '045',
                            'msg': 'Código de producto papel no valido.',
                        }
        else:
            return {
                'code': '046',
                'msg': 'El estado de la orden de fabricación no es valido. La orden debe estar en estado progreso en Odoo',
            }

        
    def _validator_update(self):
        res = self._validator_create()
        for key in res:
            if "required" in res[key]:
                del res[key]["required"]
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

    def _to_json(self, production):
        res = {
            "id" : production.id,
            "name": production.name,
            "product_id": production.product_id.id,
            "product_name": production.product_id.name,
            "state": production.state,
            "company_id": production.company_id.id,
            "company_name": production.company_id.name,
            "date_planned_start": str(production.date_planned_start),
            "routing_id": production.routing_id.id,
            #"routing_name": production.routing_id.name,
        }
        return res
