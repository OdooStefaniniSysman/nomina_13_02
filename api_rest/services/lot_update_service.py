
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
    _name = "stock.picking.service"
    _usage = "ActualizacionLotesPapel"
    _collection = "base.rest.thomasgregandsons.private.services"
    _description = """
        picking Services
        Access to the partner services is only allowed to authenticated users.
        If you are not authenticated go to <a href='/web/login'>Login</a>
    """
    
    def get(self, _id):
        """
        Get picking's informations
        """
        picking = self.env["stock.picking"].browse(_id)
        return self._to_json(picking)

    def search(self, name):
        """
        Searh picking by name
        """
        pickings = self.env["stock.picking"].name_search(name)
        pickings = self.env["stock.picking"].browse([i[0] for i in pickings])
        rows = []
        res = {"count": len(pickings), "rows": rows}
        for picking in pickings:
            rows.append(self._to_json(picking))
        return res
    
    def _get(self, _id):
        return self.env["stock.picking"].browse(_id)

    def _get_document(self, _id):
        return self.env["stock.picking"].browse(_id)

    # Validator
    def _validator_return_get(self):
        res = self._validator_create()
        #res.update({"id": {"type": "integer", "required": True, "empty": False}})
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
            "msg": {"type": "string", "required": False, "empty": True},
            "code": {"type": "string", "required": False, "empty": True},
            "name": {"type": "string", "required": False, "empty": True},
            "origin": {"type": "string", "required": False, "empty": True},
            "company_name": {"type": "string", "required": False, "empty": True},
            "scheduled_date": {"type": "string", "required": False, "empty": True},
            "state": {"type": "string", "required": False, "empty": True},
            "move_line_ids_without_package" : {
                "type": "list",
                "schema":{
                    "type" : "dict",
                    "schema":{
                        "product_id" : {"type": "integer", "required": False, "empty": True},
                        "qty_done" : {"type": "float", "required": False, "empty": True},
                        "lot_id" : {"type": "integer", "required": False, "empty": True},
                    },
                },
            },

        }
        return res

    def _validator_return_create(self):
        return self._validator_return_get()
    
    
    def update(self, **params):
        """
        Update lot papper consumables informations
        """
        keys = ['name','move_line_ids_without_package']
        for key in keys:
            if key not in params:
                _logger.error('****************************keys+++++++++++++++++')
                _logger.error(keys)
                return {
                    'code': '041',
                    'msg': 'No están bien definidos los nombres de los campos en el json!',
                }
        if not params.get('name'):
            return {
                'code': '042',
                'msg': 'Debe enviar el número de orden de fabricación en campo name!',
            }
        if not params.get('move_line_ids_without_package'):
            return {
                'code': '043',
                'msg': 'Debe enviar lleno el campo move_line_ids_without_package',
            }
        
        name = params.pop('name')
        move_line = params.pop('move_line_ids_without_package')
        for lines in move_line:
            _logger.error(params)
            picking_id = self.env['stock.picking'].search([('name','=',name)])
            _logger.error('****************************\jn+++++++++++++++++')
            _logger.error(picking_id)
            if picking_id.state == 'assigned':
                _logger.error(picking_id.state)
                for move in picking_id.move_line_ids_without_package:
                    _logger.error('****************************\product_id+++++++++++++++++')
                    _logger.error(lines.get('product_id'))
                    _logger.error('****************************\lot_id+++++++++++++++++')
                    _logger.error(lines.get('lot_id'))
                    if move.product_id.is_tracking_papper_api and move.product_id.id == lines.get('product_id'):
                        _logger.error('Entrando con producto valido')
                        try:
                            move.sudo().write({'lot_id': lines.get('lot_id'),'qty_done': lines.get('qty_done')})
                            _logger.error('+++++++++++++++++++++++++++++++++++++++lot_id')
                            _logger.error(params.get('lot_id'))
                        except Exception as e:
                            _logger.error(e)
                            _logger.error('Actualizado con exito')
                        return {
                                'code': '021',
                                'msg': 'Lote actualizada con exito!',
                            }
                    else:
                        return {
                                'code': '045',
                                'msg': 'Código de producto papel no valido.',
                            }
            else:
                return {
                    'code': '046',
                    'msg': 'El estado del movimiento no es valido. El movimiento debe estar en estado hecho en Odoo',
                }

    
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

    def _to_json(self, picking):
        _logger.error('-------------------------test-----------------')
        res = {
            "id" : picking.id,
            "name": picking.name,
            "origin": picking.origin,
            "company_name": picking.company_id.name,
            "scheduled_date": str(picking.scheduled_date),
            "state": picking.state,
        }
        return res
