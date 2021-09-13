# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class HrEmployeePrivate(models.Model):
    _inherit = "hr.employee"

    @api.model
    def create(self, vals):
        """ Creating Binders While Creating Employee """
        if vals.get("identification_id"):
            identification = vals.get("identification_id")
            for data in self.env["hr.employee"].search([]):
                if data.identification_id == identification:
                    raise ValidationError(_("This Identification No. Already exist"))
            company = vals.get("company_id")
            obj = self.env["documents.folder"]
            binder_parent = self.env.ref(
                "employee_documents.documents_hr_employees_folder"
            )
            values = {
                "name": identification,
                "parent_folder_id": binder_parent.id,
                "company_id": company,
            }
            obj.create(values)
        return super(HrEmployeePrivate, self).create(vals)

    def write(self, vals):
        """ Creating Binders While Editing The Employee"""
        if vals.get("identification_id"):
            identification = vals.get("identification_id")
            for data in self.env["hr.employee"].search([]):
                if data.identification_id == identification:
                    raise ValidationError(_("This Identification No. Already exist"))
            company = (
                vals.get("company_id")
                if vals.get("company_id")
                else self._origin.company_id
            )
            obj = self.env["documents.folder"]
            binder_parent = self.env.ref(
                "employee_documents.documents_hr_employees_folder"
            )
            values = {
                "name": identification,
                "parent_folder_id": binder_parent.id,
                "company_id": company.id,
            }
            obj.create(values)
        return super(HrEmployeePrivate, self).write(vals)


class IrAttachment(models.Model):
    _inherit = "ir.attachment"

    @api.model_create_multi
    def create(self, vals_list):
        """ Creating Documents """
        res = super(IrAttachment, self).create(vals_list)
        if not res.res_field and res.res_model == "hr.employee":
            res_id = res.res_id
            obj = self.env["documents.document"]
            emp_obj = self.env["hr.employee"].browse(res_id)
            folder = (
                self.env["documents.folder"]
                .search([("name", "=", emp_obj.identification_id)])[0]
                .id
            )
            vals = {
                "attachment_id": res.id,
                "folder_id": folder,
                "company_id": emp_obj.company_id.id,
            }
            obj.create(vals)
        return res
