#Luis Felipe Paternina
from odoo import models, fields, api, _
from odoo.osv import expression
from odoo.exceptions import UserError
import base64

import logging

logger = logging.getLogger(__name__)


class FieldService(models.Model):
    _inherit = 'project.task'

    phone =  fields.Char(related="partner_id.phone",string="Télefono",tracking=True)    
    customer_email = fields.Char(related="partner_id.email",string="Correo Electrónico del Cliente",tracking=True)
    spare_parts = fields.Selection(related="partner_id.approver_type",string="Repuestos",tracking=True)
    team_to_check = fields.Many2one('maintenance.equipment',string="Equipo a Revisar", tracking=True)
    serial = fields.Char(related="team_to_check.serial_no",string="Serial",tracking=True)
    brand = fields.Char(related="team_to_check.brand_maintenance", string="Marca", tracking=True)
    model = fields.Char(related="team_to_check.model",string="Modelo",tracking=True)
    machine_location = fields.Char(related="team_to_check.location",string="Ubicación de la Maquina",tracking=True)
    type_request = fields.Selection([('servicio de garantia','Servicio de Garantía'),('servicio nuevo','Servicio Nuevo'),('alistamiento','Alistamiento')], string="Tipo de Solicitud")
    type_service = fields.Selection([('correctivo','Correctivo'),('preventivo','Preventivo'),('instalacion de maquina','Instalación de Maquina'),('alistamiento','Alistamiento'),('instalacion de repuesto','Instalación de Repuesto'),('garantia','Garantía')], string="Tipo de Mantenimiento")
    product_id =  fields.Many2one('product.product', string="Producto")
    request_id = fields.Many2one('maintenance.request', 'Peticion')
    name = fields.Char(string="Titulo de la Tarea",readonly="True")
    partner_mobile = fields.Char(readonly="True")
    covers_and_chassis = fields.Boolean(string="Revisión de Cubiertas y Chasis")
    electronic_cards = fields.Boolean(string="Revisión Tarjetas Electrónicas")      
    electronic_settings = fields.Boolean(string="Revisión Ajustes Electrónicos")
    transportation_systems = fields.Boolean(string="Revisión de Sistema de Transporte")
    electrical_wiring = fields.Boolean(string="Revisión Cableado Elétrico")    
    engine_overhaul = fields.Boolean(string="Revisión de Motores")
    valves_and_solenoids = fields.Boolean(string="Revisión de Válvulas y Solenoides")    
    accessories = fields.Boolean(string="Revisión Accesorios")
    mechanical_adjustments = fields.Boolean(string="Revisión Ajustes Mecánicos")
    machine_ok = fields.Boolean(string="Maquina OK")     
    description_maintenance = fields.Text(string="Descripción de la Reparación o Instalación")    
    machine_change = fields.Boolean(string="Requiere Cambio de Maquina")    
    requires_spare_parts = fields.Boolean(string="Requiere Repuestos")
    feeding_systems = fields.Boolean(string="Revisión Sistemas de Alimentación")
    repair = fields.Text(string="Descripción de la Reparación")
    repair_setting = fields.Text(string="Descripción de la Reparación")
    sign = fields.Binary(string="Firma")
    plate_of_inventory = fields.Char(string="Placa de Inventario", related="team_to_check.inventory_plate")
    equipment_branch = fields.Many2one(string="Sucursal", related="team_to_check.branch")
    branch_address = fields.Char(string="Dirección de Sucursal", related="team_to_check.address")
    sap_code = fields.Char(related="partner_id.sap", string="Código SAP")
    finally_with_nov = fields.Boolean(string="Finalizar con Novedad")
    sign_by = fields.Char(string="Firmado Por")
    job_id_tst = fields.Char(string="Cargo")
    email_by = fields.Char(string="Correo")
    accident = fields.Boolean(string="Accidente")
    bad_driving = fields.Boolean(string="Mal Manejo")
    standard_use = fields.Boolean(string="Uso normal")
    img_incontec_tst = fields.Binary(related="company_id.img_incontec")
    img_logo_tst = fields.Binary(related="company_id.logo_tst")
    stage_id_maintenance = fields.Char(string="Estado del Mantenimiento")
    office_code_tst = fields.Char(related="team_to_check.office_code", string="Código de Oficina - Sucursal")
    type_of_guarantee_tst = fields.Selection([('venta','Garantía por Venta'),('mantenimiento','Garantía por Mantenimiento')], string="Tipo de Garantía",tracking=True)
    res_city_id = fields.Many2one('res.city', string="Ciudad", related="team_to_check.branch")
       

    ################################################################
    ################################################################
    def action_new_quotation(self):
        action = self.env.ref("sale_crm.sale_action_quotations_new").read()[0]
        vals = {
            'product_id': self.product_id.id,
            'name': self.name           
        }
        action['context'] = {            
            'search_default_partner_id': self.partner_id.id,
            'default_partner_id': self.partner_id.id,
            'default_origin': self.name,
            'default_company_id': self.company_id.id or self.env.company.id,
            'default_sheet_id': self.id,
            'default_order_line': [(0, 0, vals)],
        }       
        return action
    
    def _fsm_create_sale_order(self):
        """ Create the SO from the task, with the 'service product' sales line and link all timesheet to that line it """
        if not self.partner_id:
            raise UserError(_('The FSM task must have a customer set to be sold.'))

        SaleOrder = self.env['sale.order']
        if self.user_has_groups('project.group_project_user'):
            SaleOrder = SaleOrder.sudo()

        domain = ['|', ('company_id', '=', False), ('company_id', '=', self.company_id.id)]
        team = self.env['crm.team'].sudo()._get_default_team_id(domain=domain)
        sale_order = SaleOrder.create({
            'partner_id': self.partner_id.id,
            'company_id': self.company_id.id,
            'sequence_maintenance': self.name,
            'date_of_attention': self.planned_date_begin,
            'type_of_servicetst': self.type_service,
            'technical_tst': self.user_id.id,
            'office_code': self.office_code_tst,
            'address_branch_tst': self.branch_address,
            'description_maintenance': self.description_maintenance,
            'stage_maintenance': self.stage_id_maintenance,
            'branch_tst': self.equipment_branch.id,
            'type_of_guarantee_sale': self.type_of_guarantee_tst,
            'machine_tsts': self.team_to_check.id,
            'serial': self.serial,
            'brand': self.brand,
            'model_tst': self.model,
            'analytic_account_id': self.project_id.analytic_account_id.id,            
            'team_id': team.id if team else False
        })
        sale_order.onchange_partner_id()

        # write after creation since onchange_partner_id sets the current user
        sale_order.write({'user_id': self.user_id.id})

        self.sale_order_id = sale_order

    def _fsm_create_sale_order_line(self):
        #_logger.error('++++++++++++++++++++++++++++++++++\n**garantia**********')
        #_logger.error(self.type_service)
        
            
        if self.type_service == 'preventivo':
            #_logger.error('1++++++++++++++++++++++++++++++++++\n**garantia**********')
            sale_order_line = self.env['sale.order.line'].sudo().create({
                'order_id': self.sale_order_id.id,
                'product_id': self.project_id.timesheet_product_id.id,
                'project_id': self.project_id.id,
                'task_id': self.id,
                'product_uom_qty': 1.0,
                'product_uom': self.project_id.timesheet_product_id.uom_id.id,
                'price_unit': self.team_to_check.maintenance_value,
            })
            self.write({
                'sale_line_id': sale_order_line.id,
            })
            return super(FieldService, self)._fsm_create_sale_order_line()
        elif self.type_service == 'garantia' and self.project_id.timesheet_product_id.type == 'product':
            #_logger.error('2++++++++++++++++++++++++++++++++++\n**garantia**********')
            #_logger.error(self.type_service)
            sale_order_line = self.env['sale.order.line'].sudo().create({
                'order_id': self.sale_order_id.id,
                'product_id': self.project_id.timesheet_product_id.id,
                'project_id': self.project_id.id,
                'task_id': self.id,
                'product_uom_qty': 0,
                'product_uom': self.project_id.timesheet_product_id.uom_id.id,
                'price_unit': self.team_to_check.maintenance_value_corrective,
            })
            self.write({
                'sale_line_id': sale_order_line.id,
            })
        elif self.type_service == 'correctivo':
            #_logger.error('3++++++++++++++++++++++++++++++++++\n**garantia**********')
            sale_order_line = self.env['sale.order.line'].sudo().create({
                'order_id': self.sale_order_id.id,
                'product_id': self.project_id.timesheet_product_id.id,
                'project_id': self.project_id.id,
                'task_id': self.id,
                'product_uom_qty': 1.0,
                'product_uom': self.project_id.timesheet_product_id.uom_id.id,
                'price_unit': self.team_to_check.maintenance_value_corrective,
            })
            self.write({
                'sale_line_id': sale_order_line.id,
            })
            return super(FieldService, self)._fsm_create_sale_order_line()

        
    
    ######################## crear cotización desde field service ###############################
    def create_cot(self):
        domain = [('sale_ok', '=', True), '|', ('company_id', '=', self.company_id.id), ('company_id', '=', False)]
        if self.project_id and self.project_id.timesheet_product_id:
            domain = expression.AND([domain, [('id', '!=', self.project_id.timesheet_product_id.id)]])
        deposit_product = self.env['ir.config_parameter'].sudo().get_param('sale.default_deposit_product_id')
        if deposit_product:
            domain = expression.AND([domain, [('id', '!=', deposit_product)]])
        product_id = self.env['product.product'].search(domain)
        line = []    
        for product in product_id:
            product_map = {sol.product_id.id: sol.product_uom_qty for sol in self.sudo().sale_order_id.order_line}
            fsm_quantity = product_map.get(product.id, 0)
            dic = {
                'product_id': product.id,
                'name': product.name,
                'product_uom': product.uom_id.id,
                'product_uom_qty': fsm_quantity
            }
            line.append((0,0,dic))
        vals = {            
            'partner_id': self.partner_id.id,          
            'order_line': line
        }        
        so = self.env['sale.order'].create(vals)
        print('Pater', so.id, so.name)

   
    #cancelar peticion de mantenimiento desde field service//
    def cancel_field_service(self):
        peticion = self.request_id
        if peticion:
            peticion.button_finalizada()

    def confim_cotización(self):
        peticion = self.request_id
        if peticion:
            peticion.button_finalizada()

    def confim_marcar_garantia_como_hecho(self):
        peticion = self.request_id
        if peticion:
            peticion.button_marcar_como_hecho()                

    def finally_maintenance_request(self):
        # peticion_mantenimiento = self.env['maintenance.request'].search([('name','=',self.name)],limit=1)
        peticion_mantenimiento = self.request_id
        if peticion_mantenimiento:
            peticion_mantenimiento.button_marcar_como_hecho()
            self.create_attachment()
            
    def action_fsm_validate(self):
        task = super(FieldService, self).action_fsm_validate()
        self.finally_maintenance_request()        
        return task

    def create_attachment(self):
        self.ensure_one()
        request_id = self.request_id
        if request_id:
            template = self.env.ref('industry_fsm_report.mail_template_data_send_report')
            attachment = self._create_attachment(template.id, self.id)
            if attachment:
                request_id.write({'attachment_id': attachment.id})

    def _create_attachment(self, template_id, res_id):
        template = self.env['mail.template'].browse(template_id)
        if template.report_template:
            report_name = template._render_template(template.report_name, template.model, res_id)
            report = template.report_template
            report_service = report.report_name

            if report.report_type in ['qweb-html', 'qweb-pdf']:
                result, format = report.render_qweb_pdf([res_id])
            else:
                res = report.render([res_id])
                if not res:
                    raise UserError(_('Unsupported report type %s found.') % report.report_type)
                result, format = res

            result = base64.b64encode(result)
            if not report_name:
                report_name = 'report.' + report_service
            ext = "." + format
            if not report_name.endswith(ext):
                report_name += ext

            attachment_data = {
                'name': report_name,
                'datas': result,
                'type': 'binary',
                'res_model': template.model,
                'res_id': res_id,
            }
            attachment_id = self.env['ir.attachment'].sudo().create(attachment_data)
            return attachment_id   
        else:
            return False