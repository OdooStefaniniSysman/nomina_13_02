# -*- coding: utf-8 -*-

import base64
from datetime import date, datetime
import os
import io
from typing import BinaryIO
import xlsxwriter

from odoo import models, fields, api, _

file_type_dict = {
    'csv': 'text/csv',
    'xls': 'application/vnd.ms-excel',
    'xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    'ods': 'application/vnd.oasis.opendocument.spreadsheet',
}

field_type_dict = {
    'boolean': bool,
    'monetary': float,
    'datetime': datetime,
    'many2many': tuple,
    'many2one': int,
    'selection': str,
    'integer': int,
    'html': str,
    'many2one_reference': None,
    'text': str,
    'one2many': tuple,
    'reference': None,
    'binary': BinaryIO,
    'float': float,
    'date': date,
    'char': str,
}


class BaseModelImport(models.TransientModel):
    _name = 'base.model.import'
    _description = 'Base Model Import'

    data = fields.Binary('Data', attachment=False)
    name = fields.Char('Name',)
    filedata = fields.Binary('File Data', readonly=True, attachment=False)
    filename = fields.Char('File Name',)
    model_id = fields.Many2one('ir.model', required=True, default=lambda self: self.env.ref('mrp.model_mrp_workcenter_productivity'))
    state = fields.Selection([('choose', 'choose'), ('get', 'get')], default='choose')

    def action_import(self):
        this = self[0]

        out = self._import_data(self._read_file())

        this.write({
            'state': 'get',
            'filedata': out,
            'filename': '%s.xlxs' % self.model_id.model.replace('.','_')
        })

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'base.model.import',
            'view_mode': 'form',
            'res_id': this.id,
            'views': [(False, 'form')],
            'target': 'new',
        }

    def _read_file(self):
        file = base64.b64decode(self.data)
        fileformat = os.path.splitext(self.name)[-1][1:].lower()
        file_type = file_type_dict.get(fileformat, None)

        vals = {
            'res_model': self.model_id.model,
            'file': file,
            'file_name': self.name,
            'file_type': file_type,
        }

        import_id = self.env['base_import.import'].create(vals)

        options = {
            # 'advanced': True,
            # 'date_format': '',
            # 'datetime_format': '',
            # 'encoding': '',
            # 'fields': [],
            # 'float_decimal_separator': '.',
            # 'float_thousand_separator': ',',
            'headers': True,
            # 'keep_matches': False,
            # 'limit': 2000,
            # 'name_create_enabled_fields': {},
            'quoting': '"',
            # 'separator': '',
            # 'skip': 0
        }

        return import_id._read_file(options)

    def _import_data(self, source):
        # Create an in-memory output file for the new workbook.
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet()

        reader = [row for row in source]
        header = reader[0]
        content = reader[1:]

        lis = []
        for c in content:
            dic = {}
            for i, h in enumerate(header):
                dic[h] = c[i] or False
                # Write Header
                worksheet.write(0, i, h)
            lis.append(dic)
        row = 1
        for l in lis:
            try:
                # Update
                if l.get('id'):
                    model_obj = False
                    id_int = l.get('id') if isinstance(l.get('id'), int) else self.env.ref(l.get('id')).id
                    model_obj = self.env[self.model_id.model].browse(id_int)
                    del l['id']
                    nl = self._field_type(l, self.model_id)
                    # Check field type
                    model_obj.write(nl)
                # Create
                else:
                    model_obj = self.env[self.model_id.model]
                    nl = self._field_type(l, self.model_id)
                    model_obj.create(l)
            except Exception as error:
                count = 0
                for j, k in l.items():
                    worksheet.write(row, count, k)
                    count += 1
                worksheet.write(row, count, str(error))
                row += 1

        # Close the workbook before streaming the data.
        workbook.close()

        # Rewind the buffer.
        output.seek(0)

        return base64.encodestring(output.read())

    def _field_type(self, lis, model):
        new_lis = lis
        for i, l in lis.items():
            field = self.env['ir.model.fields'].search([('model_id','=',model.id),('name','=',i)])
            if not field:
                continue
            ttype = field_type_dict.get(field.ttype, None)
            if not isinstance(l, ttype):
                new_lis[i] = self._field_type_modify(l, field.ttype)
        return new_lis

    def _field_type_modify(self, value, ttype):
        if ttype == 'integer':
            value = int(value)
        if ttype == 'many2one':
            value = int(value)
        return value
