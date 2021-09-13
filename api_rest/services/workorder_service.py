
# Copyright 2018 ACSONE SA/NV
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
from odoo.addons.base_rest.components.service import to_bool, to_int
from odoo.addons.component.core import Component
from odoo import api, fields, models, SUPERUSER_ID, _
from datetime import datetime
import logging
import json
import datetime

_logger = logging.getLogger(__name__)


class Service(Component):
    _inherit = "base.rest.service"
    _name = "workorder.service"
    _usage = "ActualizacionTiempos"
    _collection = "base.rest.thomasgregandsons.private.services"
    _description = """
        Workorder Services
        Access to the partner services is only allowed to authenticated users.
        If you are not authenticated go to <a href='/web/login'>Login</a>
    """
    
    def get(self, _id):
        """
        Get Workorder's informations
        """
        workorder = self.env["mrp.workorder"].browse(_id)
        return self._to_json(workorder)

    def search(self, name):
        """
        Searh workorder by name
        """
        workorders = self.env["mrp.workorder"].name_search(name,limit=100)
        workorders = self.env["mrp.workorder"].browse([i[0] for i in workorders])
        rows = []
        res = {"count": len(workorders), "rows": rows}
        for workorder in workorders:
            rows.append(self._to_json(workorder))
        return res


    def _get(self, name, workcenter_id):
        production_id = self.env['mrp.production'].search([('name','=',name)])
        workcenter_id = self.env['mrp.workorder'].search([
            ('production_id','=',production_id.id),
            ('workcenter_id','=',workcenter_id)
        ],limit=1, order="id desc")
        return workcenter_id

    def _get_document(self, _id):
        return self.env["mrp.workorder"].browse(_id)

    

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
            "product_id": {"type": "integer", "required": False, "empty": True},
            "production_id": {"type": "integer", "required": False, "empty": True},
            "production_name": {"type": "string", "required": False, "empty": True},
            "workcenter_id": {"type": "string", "required": False, "empty": True},
            "company_name": {"type": "string", "required": False, "empty": True},
            "date_planned_start": {"type": "string", "required": False, "empty": True},
            "state": {"type": "string", "required": False, "empty": True},
            "workcenter_id" : {"type": "integer", "required": False, "empty": True},
            "time_ids" : {
                "type": "list",
                "schema":{
                    "type" : "dict",
                    "schema":{
                        "workcenter_id" : {"type": "integer", "required": False, "empty": True},
                        "date_start" : {"type": "string", "required": False, "empty": True},
                        "date_end" : {"type": "string", "required": False, "empty": True},
                        "loss_id" : {"type": "integer", "required": False, "empty": True},
                    },
                },
            },

        }
        return res

    def _validator_return_create(self):
        return self._validator_return_get()
    
    
    def update(self, **params):
        """
        Update workorder time_ids informations
        """

        keys = ['name','time_ids']
        for key in keys:
            if key not in params:
                return {
                    'code': '041',
                    'msg': 'No están bien definidos los nombres de los campos en el json!',
                }
        """
        for time in params.get('time_ids'):
            keys = ['date_start','date_end','loss_id','workcenter_id']
            if key not in time:
                return {
                    'code': '042',
                    'msg': 'No están bien definidos los nombres de los campos en el json!',
                }
        """
        if not params.get('time_ids'):
            return {
                'code': '043',
                'msg': 'Debe enviar la lista de tiempos dentro del parametro time_ids!',
            }
        time_ids = params.pop('time_ids')
        production_name = params.pop('name')
        workorder_vals = params
        for line in time_ids:
            lost_name = line.get('loss_id')
            productivity_loss = self.env['mrp.workcenter.productivity.loss'].search([('code_tracking','=',lost_name)])
            line['loss_id'] = productivity_loss.id
            date_start = line.get('date_start')
            _logger.error("date_start---------------------------------------")
            date_start = datetime.datetime.strptime(date_start, '%Y-%m-%d %H:%M:%S') + datetime.timedelta(hours=5)
            _logger.error(date_start)
            line['date_start'] = date_start
            date_end = line.get('date_end')
            _logger.error("date_end---------------------------------------")
            date_end = datetime.datetime.strptime(date_end, '%Y-%m-%d %H:%M:%S') + datetime.timedelta(hours=5)
            _logger.error(date_end)
            line['date_end'] = date_end
            time_lines = [(5,0,0)]
            _logger.error('****************************\jn+++++++++++++++++')
            _logger.error(line)
            production_id = self.env['mrp.production'].search([('name','=',production_name)])
            if production_id.state == 'progress':
                workcenter_id = self.env['mrp.workorder'].search([
                    ('production_id','=',production_id.id),
                    ('workcenter_id','=',line.get('workcenter_id'))
                ],limit=1, order="id desc")
                a = ((0, 0, line))
                time_lines.append(a)
                workorder_vals['time_ids'] = time_lines
                try:
                    _logger.error(workorder_vals)
                    workcenter_id.write(workorder_vals)
                except:
                    return {
                        'code': '044',
                        'msg': 'Ocurrio un error durante la actualización de los tiempos!',
                    }
        return {
            'code': '021',
            'msg': 'Registro de tiempo actualizo con exito!',
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

    def _to_json(self, workorder):
        res = {
            "id" : workorder.id,
            "name": workorder.name,
            "production_id": workorder.production_id.id,
            "workcenter_name": workorder.workcenter_id.name,
            "production_name": workorder.production_id.name,
            "company_name": workorder.company_id.name,
            "date_planned_start": str(workorder.date_planned_start),
            "state": workorder.state,
        }
        return res
