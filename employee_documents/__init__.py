# -*- coding: utf-8 -*-
from . import models
from odoo import api, SUPERUSER_ID


def _assign_binders(cr, registry):
    """ Setting Identification ID For Employees """
    env = api.Environment(cr, SUPERUSER_ID, {})
    binder_parent = env.ref('employee_documents.documents_hr_employees_folder')
    obj = env['documents.folder']
    # For employees, who already have Identification ID
    has_identification_id = env['hr.employee'].search([('identification_id', '!=', False)])
    if has_identification_id:
        for employee in has_identification_id:
            values = {'name': employee.identification_id, 'parent_folder_id': binder_parent.id,
                      'company_id': employee.company_id.id}
            obj.create(values)
    # For employees who don't have Identification ID
    no_identification_id = env['hr.employee'].search([('identification_id', '=', False)])
    if no_identification_id:
        for employees in no_identification_id:
            employees.identification_id = employees.name


def uninstall_hook(cr, registry):
    """ Removing the Identification No. set by this module"""
    env = api.Environment(cr, SUPERUSER_ID, {})
    module_datas = env['hr.employee'].search([])
    for data in module_datas:
        if data.identification_id == data.name:
            data.identification_id = False
