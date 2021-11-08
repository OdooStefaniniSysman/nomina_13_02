#Luis Felipe Paternina-
from odoo import models, fields, api, _
from datetime import datetime
from datetime import timedelta
from odoo.exceptions import ValidationError,RedirectWarning

class MaintenanceRequest(models.Model):
    _inherit = 'maintenance.request'    
    
    equipment_id = fields.Many2one('maintenance.equipment', string="Máquina")
    task_id = fields.Many2one('project.task', 'Tarea')
    service_order = fields.Char(string="Orden del Servicio",tracking=True)
    customer = fields.Many2one('res.partner', string="Cliente", tracking=True)
    city = fields.Char(related="customer.city",string="Ciudad", tracking=True)
    approver_name = fields.Char(string="Nombre del Aprobador", tracking=True)
    approver_email = fields.Char(string="Correo del Aprobador", tracking=True)
    contract_code = fields.Char(related="customer.no_contract", string="Código del Contrato", tracking=True)
    end_date_contract = fields.Date(related="customer.end_date_contract", string="Fecha Fin del Contrato",tracking=True)
    approver_type_contract = fields.Selection(related="customer.approver_type", string="Tipo de aprobación para repuestos",tracking=True)
    brand_machine  = fields.Char(related="equipment_id.brand_maintenance",string="Marca")
    serie = fields.Char(related="equipment_id.serial_no",tracking=True)
    model_machine = fields.Char(related="equipment_id.model", tracking=True, string="Modelo")
    type_of_maintenance = fields.Selection([('correctivo','Correctivo'),('preventivo','Preventivo'),('instalacion de maquina','Instalación de Maquina'),('alistamiento','Alistamiento'),('instalacion de repuesto','Instalación de Repuesto'),('garantia','Garantía')], string="Tipo de Mantenimiento")
    machine_location = fields.Char(related="equipment_id.location",string="Ubicación de la Maquina",tracking=True)
    type_request_maintenance = fields.Selection([('servicio de garantia','Servicio de Garantía'),('servicio nuevo','Servicio Nuevo'),('alistamiento','Alistamiento')], string="Tipo de Solicitud")    
    attachment_id = fields.Many2one('ir.attachment', 'Adjunto')
    datetime_now=fields.Datetime('Fecha y hora Actual',tracking=True, default= fields.Datetime().now())
    total_days=fields.Integer(string="TOTAL DAYS")
    name = fields.Char(required=False)
    check_mant_day = fields.Boolean('Check_mantenimiento')
    equipment_branch = fields.Many2one(string="Sucursal", related="equipment_id.branch",tracking=True)
    branch_address = fields.Char(string="Dirección de Sucursal", related="equipment_id.address",tracking=True)
    plate = fields.Char(string="Placa de Inventario", related="equipment_id.inventory_plate",tracking=True)
    description_of_maintenance = fields.Text(string="Descripción", tracking=True)
    mantenimientos_proces = fields.Text('Mantenimiento en proceso',tracking=True)    
    preventive = fields.Char(string="Preventivo")
    corrective = fields.Char(string="Correctivo")
    department_add = fields.Many2one(related="equipment_id.department", string="Departamento",tracking=True)
    city_machine = fields.Many2one(related="equipment_id.branch", string="Ciudad",tracking=True)
    branch_machine_tst = fields.Char(string="Sucursal", related="equipment_id.branch_tst",tracking=True)
    sequence_machine = fields.Integer(related="stage_id.sequence")
    type_of_guarantee = fields.Selection([('venta','Garantía por Venta'),('mantenimiento','Garantía por Mantenimiento')], string="Tipo de Garantía",tracking=True)
    maintenance_worksheet = fields.Many2one('maintenance.request', string="Hoja de trabajo relacionada con garantía",tracking=True)
    sap_code_sap = fields.Char(related="customer.sap")
    stage_id_related = fields.Char(related="stage_id.name", string="Estado de la Petición")
    office_code_tst = fields.Char(related="equipment_id.office_code", string="Código de Oficina - Sucursal")
    machine_rental = fields.Boolean(string="Máquina en Contrato de Alquiler", related="equipment_id.rental_contract")
    

    @api.onchange('customer')
    def onchange_partner_id(self):
        for rec in self:
            return {'domain':{'equipment_id':[('partner_client_id', '=', rec.customer.id)]}}

    @api.model
    def create(self, vals):
        
        #Ventana de advertencia al guardar, si una máquina está en mantenimiento
        if vals.get('schedule_date') and vals.get('datetime_now'):
            d1=datetime.strptime(str(vals.get('datetime_now')),'%Y-%m-%d %H:%M:%S') 
            d2=datetime.strptime(str(vals.get('schedule_date')),'%Y-%m-%d %H:%M:%S')
            d3=d2-d1 
            domain = [('equipment_id', '=', vals.get('equipment_id'))]
            am = self.env['maintenance.request'].search(domain)
            if  d3.days <= 15 and am:
                vals.update(check_mant_day= True)
            else:
                vals.update(check_mant_day= False)

        name = self.env['ir.sequence'].next_by_code('maintenance.request') or _('Nuevo')

        if vals.get('type_of_maintenance') == 'correctivo':
            vals.update(name='MC'+name)
        elif vals.get('type_of_maintenance') == 'preventivo':
            vals.update(name='MP'+name)    
        else:
            vals.update(name=name)                   
        return super(MaintenanceRequest, self).create(vals)      

    def write(self, vals):

        if vals.get('stage_id'):
            #progress = self.env.ref('maintenance_thomas.stage_7')            
            progress = self.env.ref('maintenance.stage_1')            
            if progress and vals.get('stage_id') == progress.id:
                self.create_task()
        if vals.get('schedule_date') or vals.get('duration') or vals.get('customer') or vals.get('equipment_id') or vals.get('type_of_maintenance') or vals.get('type_request_maintenance') or vals.get('user_id') or vals.get('stage_id_related') :
            self.write_task(vals)

        if vals.get('type_of_maintenance') == 'correctivo':
            vals.update(name='MC '+self.name.lstrip("MP "))
        elif vals.get('type_of_maintenance') == 'preventivo':
            vals.update(name='MP '+self.name.lstrip("MC "))    
               
        return super(MaintenanceRequest, self).write(vals)

    def create_task(self):
        for record in self:
            planned_date_begin = record.schedule_date or fields.Datetime.now()
            planned_date_end = planned_date_begin + timedelta(hours=record.duration)

            dic = {
                'request_id': record.id,
                'is_fsm': True,
                'project_id': self.env.ref('industry_fsm.fsm_project').id,
                'name': record.name,
                'brand': record.brand_machine,
                'model': record.model_machine,
                'type_request': record.type_request_maintenance,                
                'serial': record.serie,              
                'type_service': record.type_of_maintenance,
                'machine_location': record.machine_location,               
                'planned_date_begin': planned_date_begin,
                'planned_date_end': planned_date_end,
                'stage_id_maintenance':record.stage_id_related,
                'type_of_guarantee_tst': record.type_of_guarantee,
                'partner_id': record.customer.id if record.customer else False,
                'team_to_check': record.equipment_id.id if record.equipment_id else False,
                'user_id':record.user_id.id if record.user_id else False
            }
            record.task_id = self.env['project.task'].sudo().create(dic)

    def write_task(self, vals):
             
        for record in self:
            if record.task_id:
                dic = {}
                if vals.get('schedule_date') or vals.get('duration'):
                    planned_date_begin = vals.get('schedule_date') or record.schedule_date          
                    duration = vals.get('duration') or record.duration
                    try:
                        planned_date_end = datetime.strptime(planned_date_begin, '%Y-%m-%d %H:%M:%S') + timedelta(hours=duration)
                    except:
                        planned_date_end = planned_date_begin + timedelta(hours=duration)
                    dic.update(planned_date_begin=planned_date_begin)
                    dic.update(planned_date_end=planned_date_end)
                if vals.get('customer'):
                    dic.update(partner_id=vals.get('customer'))
                if vals.get('equipment_id'):
                    dic.update(team_to_check=vals.get('equipment_id'))
                if vals.get('type_of_maintenance'):
                    dic.update(type_service=vals.get('type_of_maintenance'))
                if vals.get('type_request_maintenance'):
                    dic.update(type_request=vals.get('type_request_maintenance'))
                if vals.get('user_id'):
                    dic.update(user_id=vals.get('user_id'))
                if vals.get('stage_id_related'):
                    dic.update(stage_id_maintenance=vals.get('stage_id_related'))                 
                record.task_id.write(dic)

    #cambiar de etapa
    def button_finalizada(self):
        rs = self.env['maintenance.stage'].search([('name', '=', 'FINALIZADO CON NOVEDAD')], limit=1)
        self.write({'stage_id': rs.id})

    def button_marcar_como_hecho(self):
        rs = self.env['maintenance.stage'].search([('name', '=', 'FINALIZADO')], limit=1)
        self.write({'stage_id': rs.id})        
            
   #Ventana de advertencia para verificar si una máquina está en mantenimiento
    @api.onchange('equipment_id','schedule_date')
    def calculate_date(self):
        for record in self:
            if  record.schedule_date and record.datetime_now:

                d2=record.schedule_date
                d1=fields.Datetime().now()
                d3= (d2 - d1).days
                domain = [('equipment_id', '=', record.equipment_id.id),('check_mant_day','=', True)]
                am = self.env['maintenance.request'].search(domain)
                self.mantenimientos_proces = str([x.name for x in am])
               # mr = self.env['maintenance.request'].search([domainmr])
                if  0 <= d3 <= 15 and am:
                    record.check_mant_day= True
                else:
                    record.check_mant_day= False

    

    
                    

         
         	
            



              


         
        

               

      
    
