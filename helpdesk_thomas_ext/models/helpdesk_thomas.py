# -*- coding: utf-8 -*-
from odoo import models, fields, api
import math
from odoo.exceptions import ValidationError
from datetime import datetime,date,timedelta
from odoo.osv import expression

class HelpdeskTicket(models.Model):
    _inherit = 'helpdesk.ticket'
    
    def _add_domain_service(self):
        service_obj = self.env['helpdesk.service'].search([])
        ids= []
        for service_id in service_obj:
            for groups_id in service_id.group_users_id:
                if self.env.user.id in groups_id.user_id.ids:
                    ids.append(service_id.id)
            
        return [('id','in',ids)]
    
    def _add_domain_activity(self):
        activity_obj = self.env['helpdesk.activity'].search([])
        ids= []
        for activity_id in activity_obj:
            if self.env.user.id in activity_id.users_ids.ids:
                ids.append(activity_id.id)
            
        return [('id','in',ids)]

    val_req_contact = fields.Boolean(string="Valid requirements")
    tiket_number_contract = fields.Char(string='Ticket number Legal management')
    maintenance_equipment_id = fields.Many2one(
        'maintenance.equipment',
        string='Maintenance Equipment',
        )
    equipment_model = fields.Char(string='Model')
    equipment_serial = fields.Char(string='Brand')
    # equipment_customer = fields.Char(string='Equipment related customer')
    equipment_supplier = fields.Char(string='Supplier associated to the guarantee')
    guarantee_reply = fields.Char(string='Guarantee reply')
    inventory_ubication = fields.Selection([('product in cellar', 'product in cellar'),('product at supplier location','product at supplier location')], string='Inventory ubication')
    customer_response = fields.Char(string='Customer response')

################################################################################################
    ##########################################################################################################################
    ticket_type_id = fields.Many2one(
        'helpdesk.ticket.type', "Urgencia", tracking=True)
    ticket_type = fields.Selection([('incidents', 'Incidente'),('request','Solicitud')], string='Ticket type')
    service_id = fields.Many2one('helpdesk.service', string="Servicio", domain=_add_domain_service)
    subservice_id = fields.Many2one('helpdesk.subservice', string="Subservicio")
    type_ticket_id = fields.Many2one('helpdesk.type', string="Urgencia" )
    activity_id = fields.Many2one('helpdesk.activity', string="Actividad", domain=_add_domain_activity) 
    problem = fields.Many2one('helpdesk.problem', string="Problem")
    helpdesk_id = fields.Many2one('helpdesk.helpdesk', string="Problem")
    team_id = fields.Many2one('helpdesk.team', string="Equipo de ayuda")
########################################################################################################
    group_users_id = fields.Many2one('helpdesk.groupusers', string="Group Users")
    material_type = fields.Many2one('helpdesk.material.type', string="Tipo Material")
######################################################################################################

    departament = fields.Char(compute='_get_department_user', string='Departamento')
    request_contact = fields.Many2one('res.users', string="Solicitud de tercero")
    format_archive = fields.Binary(string="Format Archive", help="FORMATO: TE-R-010'\n'PARA LAS ACTIVIDADES:'\n'Nueva Funcionalidad'\n'Ajustes y Modificaciones'\n'Correctivo - Desempe??o'\n'Correctivo - Usabilidad'\n'Correctivo - Procesamiento'\n'Reportes a la Medida'\n'Reportes en Sistema'\n'Dise??o de plantillas'\n'Construcci??n de plantillas'\n'Modificaci??n de plantillas'\n'-------------------------------------------------'\n'FORMATO: SOP-FOR-001 / SAP-FOR-003'\n'PARA LAS ACTIVIDADES:'\n'Creaci??n'\n'-------------------------------------------------'\n'FORMATO: SAP / SAP-FOR-003'\n'PARA LAS ACTIVIDADES:'\n'Modificaci??n y Reactivaci??n '\n'-------------------------------------------------'\n'FORMATO: SOP-FOR-005'\n'PARA LAS ACTIVIDADES:'\n'Eliminaci??n y Desactivaci??n'\n'Retiro de Licencia Office 365'\n'-------------------------------------------------'\n'FORMATO: TEC-FOR-003'\n'PARA LAS ACTIVIDADES:'\n'Acceso y actualizaci??n de recursos compartidos'\n'Acceso a servicios SFTP/FTP'\n'Gesti??n de las plataformas e infraestructura local'\n'Control de cambios'\n'-------------------------------------------------'\n'FORMATO: Informe de an??lisis de vulnerabilidades'\n'PARA LAS ACTIVIDADES:'\n'Gesti??n de las vulnerabilidades'\n'-------------------------------------------------'\n'FORMATO: Acta de entrega'\n'PARA LAS ACTIVIDADES:'\n'Alistamiento y entrega de equipo de computo'\n'Alistamiento y entrega de servidores")
    format_archive_filename = fields.Char("File Name")

    priority = fields.Selection([('0', 'Baja'),
                                 ('1', 'Baja'),
                                ('2', 'Media'),
                                ('3', 'Alta')], compute='_get_activity_priority',readonly=True, store=True, string="Prioridad")
    
    required_information_ticket = fields.Selection([('Si', 'Si'),
                                      ('No', 'No')], string="Informaci??n requerida Completa")

    info_security = fields.Selection([('Si', 'Si'),
                                      ('No', 'No'),], related='activity_id.info_security', string="Actividad requiere de seguridad de la informaci??n", tracking=True)
    
    info_security_scale = fields.Selection([('Si', 'Si'),
                                      ('No', 'No'),], string="Escalar a seguridad de la informaci??n", tracking=True)

    ans_date_selector = fields.Selection([('Si', 'Si'),
                                      ('No', 'No'),], string="Ans con Fecha")
    
    ans_datetime =fields.Datetime('Seleccione la fecha en la que se debe cumplir el ANS')

    resolved = fields.Selection([('Si', 'Si'),
                                      ('No', 'No'),], string="Resuelto")

    sla_check = fields.Boolean('Cumpli?? SLA', compute='_compute_sla_check')

    description_solution = fields.Char('Describa la soluci??n del ticket')

    state_record= fields.Char('Estados', compute='_get_state_label')
    check_file_document = fields.Boolean(compute='_get_check_file_document', string='Check file')
    check_info_security = fields.Boolean(compute='_get_check_file_document', string='Check file')
    check_ans_fecha = fields.Boolean(compute='_get_check_ans_fecha', string='Check file')
    
    ############################### TIEMPOS ETAPAS TECNOLOGIA
    tiempo_1ra_aprobacion = fields.Float('Tiempo etapa Nuevo')
    tiempo_2da_aprobacion = fields.Float('Tiempo etapa en revisi??n')
    tiempo_3ra_aprobacion = fields.Float('Tiempo etapa en Aprobaci??n Segurinfor')
    tiempo_aprobada_cliente = fields.Float('Tiempo etapa en espera Informaci??n de Usuario')
    tiempo_aprobada = fields.Float('Tiempo etapa en Gesti??n')
    tiempo_abierta = fields.Float('Tiempo en Etapa Abierta')
    tiempo_cerrada = fields.Float('Tiempo en Etapa Cerrada')
    tiempo_garantia = fields.Float('Tiempo en Etapa de Garant??a')
    tiempo_hora_finalizada = fields.Float('Tiempo etapa en Escalado a terceros')
    tiempo_hora_solucion = fields.Float('Tiempo solucion')
    tiempo_total=fields.Float('Tiempo Total del Proceso')
    tiempo_gestion_tecnologia = fields.Float('Gesti??n de la tecnolog??a', compute='_get_total_ans')
    sum_no_ans =  fields.Float('Tiempo que no aplica SLA', compute='_get_total_ans')
    #FECHAS ETAPAS TECNOLOGIA
    tiempo_inicial=fields.Datetime('Fecha y hora de inicio', default= fields.Datetime().now())
    fecha_hora_1ra_aprobacion = fields.Datetime('Tiempo etapa Nuevo',  default= fields.Datetime().now())
    fecha_hora_2da_aprobacion = fields.Datetime('Tiempo etapa en revisi??n')
    fecha_hora_3ra_aprobacion = fields.Datetime('Tiempo etapa en Aprobaci??n Segurinfor')
    fecha_hora_aprobada_cliente = fields.Datetime('Fecha y hora Etapa Aprobada por el Cliente')
    fecha_hora_aprobacion = fields.Datetime('Fecha y hora Etapa de Aprobaci??n')
    fecha_hora_abierta = fields.Datetime('Fecha y hora Etapa Abierta')
    fecha_hora_cerrada = fields.Datetime('Fecha y hora Etapa Cerrada')
    fecha_hora_garantia = fields.Datetime('Fecha y hora Etapa de Garant??a')
    fecha_hora_finalizada = fields.Datetime('Fecha y hora Etapa de Garant??a')
    fecha_hora_solucion = fields.Datetime('Fecha y hora Etapa de Soluci??n', tracking=True)
    ##############################Tiempos SEGURIDAD#############################################################
    tiempo_1ra_aprobacion_2 = fields.Float('Tiempo en recepci??n')
    tiempo_2da_aprobacion_2 = fields.Float('Tiempo en Autorizacion o aprobaciones')
    tiempo_3ra_aprobacion_2 = fields.Float('Tiempo Verificaci??n')
    tiempo_aprobada_cliente_2 = fields.Float('Tiempo En Devoluci??n')
    tiempo_aprobada_2 = fields.Float('Tiempo en Tercero')
    tiempo_abierta_2 = fields.Float('Tiempo en Etapa Abierta')
    tiempo_cerrada_2 = fields.Float('Tiempo en Etapa Cerrada')
    tiempo_garantia_2 = fields.Float('Tiempo en Etapa de Garant??a')
    tiempo_hora_finalizada_2 = fields.Float('Tiempo en Etapa de Garant??a')
    tiempo_hora_solucion_2 = fields.Float('Tiempo solucion')
    tiempo_total_2 =fields.Float('Tiempo Total del Proceso')
    #FECHAS ETAPAS SEGURIDAD
    tiempo_inicial_2 =fields.Datetime('Fecha y hora de inicio', default= fields.Datetime().now())
    fecha_hora_1ra_aprobacion_2 = fields.Datetime('Fecha y hora 1ra Aprobaci??n', default= fields.Datetime().now())
    fecha_hora_2da_aprobacion_2 = fields.Datetime('Fecha y hora 2da Aprobaci??n')
    fecha_hora_3ra_aprobacion_2 = fields.Datetime('Fecha y hora 3ra Aprobaci??n')
    fecha_hora_aprobada_cliente_2 = fields.Datetime('Fecha y hora Etapa Aprobada por el Cliente')
    fecha_hora_aprobacion_2 = fields.Datetime('Fecha y hora Etapa de Aprobaci??n')
    fecha_hora_abierta_2 = fields.Datetime('Fecha y hora Etapa Abierta')
    fecha_hora_cerrada_2 = fields.Datetime('Fecha y hora Etapa Cerrada')
    fecha_hora_garantia_2 = fields.Datetime('Fecha y hora Etapa de Garant??a')
    fecha_hora_finalizada_2 = fields.Datetime('Fecha y hora Etapa de Garant??a')
    fecha_hora_solucion_2 = fields.Datetime('Fecha y hora de Soluci??n')
    
    
    date_aper = fields.Datetime(string='Fecha de Apertura', required=True, readonly=True, index=True,  default=fields.Datetime.now)
    service_id_label = fields.Char(string='servicio', compute='_get_label_service_id')
    sub_service_id_label = fields.Char(string='Sub-servicio', compute='_get_label_subservice')
    team_label = fields.Char(string='Sub-servicio', compute='_get_team_label')
##################################SEGURIDAD########################################################
######################################ASEGURAMIENTO DE PRODUCTOS ######################################
    material = fields.One2many('helpdesk.material','material_ids', string='Material')
    solicitud_almacenamiento = fields.Datetime(string='Solicitud de Almacenamiento hasta: ')
    material_requiere = fields.Boolean(string='Material requiere investigaci??n')
    reporte_indemnidad = fields.Binary(string='Reporte de imdemnidad')
    producto_incompleto = fields.Binary(string='Producto incompleto, auntentico')
    acta_destruccion = fields.Binary(string='Acta de destrucci??n')
    link_video = fields.Char(string='Link de video')

#####################################RECOLECCI??N Y ENTREGAS SEGURIDAD #####################################
    nombre_servicio = fields.Char('Nombre del servicio')
    producto_entregar = fields.Char('Producto a recolectar o entregar')
    escolta_asignado_id = fields.Many2one('helpdesk.escolta', string='Escolta Asignado')
    escolta_asignado_entrega_id = fields.Many2one('helpdesk.escolta', string='Escolta Asignado')
    fecha_programacion = fields.Datetime(string='Fecha y hora de programaci??n')
##################################ORDENES DE SALIDA #########################################
    producto_articulo = fields.One2many('helpdesk.producto','producto_ids', string='Producto/articulo')
    nombre_persona_retira = fields.Char('Nombre de la persona que retira')
    destino = fields.Char('Destino')
    aprobado_jede_departamento = fields.Selection([('Si', 'Si'),
                                                    ('No', 'No'),], string="Aprobaci??n supervisor de seguridad")
    aprobado_seguridad = fields.Selection([('Si', 'Si'),
                                            ('No', 'No'),], string="Aprobado por Seguridad de informaci??n")
    aprobado_seguridad_informacion = fields.Selection([('Si', 'Si'),
                                            ('No', 'No'),], string="Aprobado por Seguridad")
    
    porteria = fields.Selection([('principal', 'Principal'),
                                      ('12', '12-80'),], string="Porter??a")
    
    devolutivo = fields.Selection([('Si', 'Si'),
                                            ('No', 'No'),], string="Devolutivo")
    
    fecha_devolucion = fields.Date(string='Fecha de devolucion')
    vigilantes_verifica_devolucion_id = fields.Many2one('helpdesk.vigilante', string='Vigilante que verifica Devoluci??n')
    vigilantes_id = fields.Many2one('helpdesk.vigilante', string='Vigilante que verifica salida')
    

#######################################INFORME ANALISIS DE AUTENTICIDAD ########################
    cliente = fields.Char('Cliente')
    producto = fields.Char('Producto')
    ubicacion_producto = fields.Char('Ubicaci??n o direcci??n del producto')
    fecha_solicitada_recoleccion = fields.Date('Fecha solicitada para recolecci??n')
    numeracion = fields.Char('Numeraci??n')
    no_sorteo = fields.Char('No del sorteo')
    serie = fields.Char('Serie')
    fraccion = fields.Char('Fracci??n')
    aprobado_gerencia_seguridad = fields.Boolean('Aprobado por gerencia de seguridad')
    analisis_tecnologia = fields.Boolean('*An??lisis de Tecnolog??a')
    verificacion_codigo_barras = fields.Selection([('cumple', 'Cumple'),
                                            ('no_cumple', 'No cumple'),
                                            ('no_aplica', 'No aplica'),], string="1. VERIFICACION CODIGO DE BARRAS: ")
    verificacion_codigo_control = fields.Selection([('cumple', 'Cumple'),
                                            ('no_cumple', 'No cumple'),
                                            ('no_aplica', 'No aplica'),], string="2. VERIFICACION CODIGO DE CONTROL:")
    verificacion_distribuidor = fields.Selection([('cumple', 'Cumple'),
                                            ('no_cumple', 'No cumple'),
                                            ('no_aplica', 'No aplica'),], string="3. VERIFICACION DEL DISTRIBUIDOR:")
    verificacion_sorteo = fields.Selection([('cumple', 'Cumple'),
                                            ('no_cumple', 'No cumple'),
                                            ('no_aplica', 'No aplica'),], string="4. VERIFICACION SORTEO:")
    verificacion_billete = fields.Selection([('cumple', 'Cumple'),
                                            ('no_cumple', 'No cumple'),
                                            ('no_aplica', 'No aplica'),], string="5. VERIFICACION N?? DE BILLETE:")
    verificacion_serie = fields.Selection([('cumple', 'Cumple'),
                                            ('no_cumple', 'No cumple'),
                                            ('no_aplica', 'No aplica'),], string="6. VERIFICACION SERIE:")
    verificacion_variable = fields.Selection([('cumple', 'Cumple'),
                                            ('no_cumple', 'No cumple'),
                                            ('no_aplica', 'No aplica'),], string="7. VER INF.VARIABLE TIRA DE CONTROL:")
    tira_control_virtual = fields.Selection([('cumple', 'Cumple'),
                                            ('no_cumple', 'No cumple'),
                                            ('no_aplica', 'No aplica'),], string="8. TIRA CONTROL VIRTUAL:")
    analisis_realizado = fields.Many2one('hr.employee', string='An??lisis realizado por')
    cargo = fields.Char(string='Cargo', compute='_get_cargo_label')
    analisis_preprensa = fields.Boolean('*An??lisis por preprensa')
    fondos_especiales = fields.Selection([('cumple', 'Cumple'),
                                            ('no_cumple', 'No cumple'),
                                            ('no_aplica', 'No aplica'),], string="A. FONDOS ESPECIALES UTILIZADOS")
    antifotocopias = fields.Selection([('cumple', 'Cumple'),
                                            ('no_cumple', 'No cumple'),
                                            ('no_aplica', 'No aplica'),], string="B. ANTIFOTOCOPIAS NULO")
    verificacion_microtextos = fields.Selection([('cumple', 'Cumple'),
                                            ('no_cumple', 'No cumple'),
                                            ('no_aplica', 'No aplica'),], string="C. VERIFICACION MICROTEXTOS")
    verificacion_impresion = fields.Selection([('cumple', 'Cumple'),
                                            ('no_cumple', 'No cumple'),
                                            ('no_aplica', 'No aplica'),], string="D. VERIFICACION DE LA IMPRESI??N LITOGRAFICA")
    cremocromaticas = fields.Selection([('cumple', 'Cumple'),
                                            ('no_cumple', 'No cumple'),
                                            ('no_aplica', 'No aplica'),], string="E. CREMOCROMATICAS")
    analisis_realizado_preprensa = fields.Many2one('hr.employee', string='An??lisis realizado por')
    cargo_preprensa = fields.Char(string='Cargo', compute='_get_cargo_label_preprensa')
    analisis_laboratorio = fields.Boolean('*An??lisis de Laboratorio')
    fluorescente_invisible = fields.Selection([('cumple', 'Cumple'),
                                            ('no_cumple', 'No cumple'),
                                            ('no_aplica', 'No aplica'),], string="A. FLUORESCENTE INVISIBLE")
    fluorescente_visible = fields.Selection([('cumple', 'Cumple'),
                                            ('no_cumple', 'No cumple'),
                                            ('no_aplica', 'No aplica'),], string="B. FLUORESCENTE VISIBLE")
    fluoranulado = fields.Selection([('cumple', 'Cumple'),
                                            ('no_cumple', 'No cumple'),
                                            ('no_aplica', 'No aplica'),], string="C. FLUORANULADO")
    reactivo_moneda = fields.Selection([('cumple', 'Cumple'),
                                            ('no_cumple', 'No cumple'),
                                            ('no_aplica', 'No aplica'),], string="D. REACTIVO A LA MONEDA")
    anulado = fields.Selection([('cumple', 'Cumple'),
                                            ('no_cumple', 'No cumple'),
                                            ('no_aplica', 'No aplica'),], string="E. ANULADO")
    sensible_borrado = fields.Selection([('cumple', 'Cumple'),
                                            ('no_cumple', 'No cumple'),
                                            ('no_aplica', 'No aplica'),], string="F. SENSIBLE AL BORRADO")
    termocromicas = fields.Selection([('cumple', 'Cumple'),
                                            ('no_cumple', 'No cumple'),
                                            ('no_aplica', 'No aplica'),], string="G. TERMOCROMICAS")
    fotocromaticas = fields.Selection([('cumple', 'Cumple'),
                                            ('no_cumple', 'No cumple'),
                                            ('no_aplica', 'No aplica'),], string="H. FOTOCROMATICAS")
    analisis_realizado_laboratorio = fields.Many2one('hr.employee', string='An??lisis realizado por')
    cargo_laboratorio = fields.Char(string='Cargo', compute='_get_cargo_label_laboratorio')
    validacion_analisis_gerente_seguridad = fields.Selection([('si', 'SI'),
                                ('no', 'NO')], string="Validaciones an??lisis gerente de seguridad", traking = True)
#########################################################INGRESO COMPA??IA VISITANTES#########################################
    area_ingreso = fields.Selection([('administrativa', 'Administrativa'),
                                            ('planta', 'Planta'),], string="Area de ingreso")
    fecha_ingreso = fields.Datetime('Fecha y Hora de ingreso')
    fecha_salida = fields.Datetime('Fecha y Hora de salida')
    registro_personas = fields.One2many('helpdesk.personas','personas_ids', string='Registro de personas')
    registro_personas_adjunto = fields.One2many('helpdesk.personas','personas_ids', string='Registro de personas (Recuerde adjuntar la o las planillas de para-fiscales)')
    aprobado_salud = fields.Boolean('Aprobado Salud ocupacional')
    #########################################################MUESTRAS#########################################
    clase_anulado = fields.Selection([('especimen', 'Esp??cimen'),
                                            ('sello', 'Sello'),], string="Clase de Anulado")
    entregar = fields.Many2one('hr.employee', string='Entregar a')
    aprobado_gerencia = fields.Boolean('Aprobado por gerencia')
    aprobado_laboratorio = fields.Boolean('Aprobado por laboratorio')
    notas_desaprobacion_laboratorio = fields.Text('Notas de desaprobaci??n laboratorio')
    requiere_devolucion = fields.Boolean('Requiere devoluci??n')
    fecha_devolucion_muestra = fields.Datetime('Fecha y hora de devoluci??n de la muestra')
    muestras_id = fields.Many2many('helpdesk.producto.muestras', string='Muestras')
###################################################SOLICITUD VIDEOS########################################
    solicitud_video_aprobado = fields.Boolean('Solicitud de video Aprobado')
    video_aprobado_entrega = fields.Boolean('Video aprobado para la entrega')
####################################################APROBADO SEGURIN#########################################
    aprobacion_segurinfo = fields.Selection([('si', 'SI'),
                                ('no', 'NO')], string="Aprobaci??n usuario Segurinfo", traking = True)
###################################################Tiempo abs################################################
  #  sla_deadline = fields.Datetime("SLA Deadline", compute='_get_deadline_ans', compute_sudo=True, help="The closest deadline of all SLA applied on this ticket")
#################################################Politica de ANS fallida#############################################
    sla_fail = fields.Boolean("Failed SLA Policy", compute='_compute_sla_fail_ticket', search='_search_sla_fail')
    activity_subservice_id = fields.Many2one('helpdesk.activity', related='activity_id.subservice_id')
    users_groups_related = fields.Many2many('res.users', string='Usuarios del grupo relacionados', related='group_users_id.user_id')
###########################################################################################################################
    @api.depends('sla_deadline','fecha_hora_solucion_2','fecha_hora_solucion')
    def _compute_sla_check(self):
        for record in self:
            if record.fecha_hora_solucion and record.sla_deadline:
                if record.fecha_hora_solucion < record.sla_deadline:
                    record.sla_check=True
                else:
                    record.sla_check=False
            elif record.fecha_hora_solucion_2 and record.sla_deadline:
                if record.fecha_hora_solucion_2 < record.sla_deadline:
                    record.sla_check=True
                else:
                    record.sla_check=False
            elif not record.fecha_hora_solucion and not record.fecha_hora_solucion_2:
                record.sla_check=False
            elif not record.sla_deadline:
                record.sla_check=False
                
    @api.depends('sla_check')
    def _compute_sla_fail_ticket(self):
        for record in self:
            now = fields.Datetime.now()
            if record.sla_deadline:
                if now < record.sla_deadline:
                    record.sla_fail = False
                else:
                    record.sla_fail = True
            
            elif record.sla_deadline:
                if now < record.sla_deadline:
                    record.sla = False
                else:
                    record.sla_fail = True

            else:
                record.sla_fail = False
    
    @api.depends('activity_id')
    def _get_activity_priority(self):
        for record in self:
            if record.activity_id.priority:
                record.priority=record.activity_id.priority
            else:
                 record.priority=False
                    
    @api.depends('ticket_type_id','activity_id','ans_datetime','subservice_id')
    def _get_deadline_ans(self):
        ans_obj_seg = self.env['helpdesk.sla'].search([('ticket_type_id','=',self.ticket_type_id.id),('activity_id.subservice_id','=',self.subservice_id.id)])
        ans_obj_tec = self.env['helpdesk.sla'].search([('ticket_type_id','=',self.ticket_type_id.id),('activity_id','=',self.activity_id.id)])
        for ans_tec_ids in ans_obj_tec:
            for record in self:
                if ans_tec_ids.ticket_type_id == record.ticket_type_id and ans_tec_ids.activity_id == record.activity_id and not record.ans_datetime :
                    record.sla_deadline=record.date_aper + timedelta(days=ans_tec_ids.time_days) + timedelta(hours=ans_tec_ids.time_hours) 
                    record.sla_status_ids = ans_obj_tec.ids
                else:
                    record.sla_deadline = False
                    
                if record.ans_datetime:            #Seleccionar tiempo de fecha manualmente en la que se debe cumplir
                    record.sla_deadline = record.ans_datetime
        
        for ans_seg_ids in ans_obj_seg:
            for record in self:
                if ans_seg_ids.ticket_type_id == record.ticket_type_id and ans_seg_ids.activity_id.subservice_id == record.subservice_id and not record.ans_datetime :
                    record.sla_deadline=record.date_aper + timedelta(days=ans_seg_ids.time_days) + timedelta(hours=ans_seg_ids.time_hours)
                    record.sla_status_ids = ans_obj_tec.ids
                else:
                    record.sla_deadline = False

                if record.ans_datetime:            #Seleccionar tiempo de fecha manualmente en la que se debe cumplir
                    record.sla_deadline = record.ans_datetime
                    
    def _sla_find(self):
        tickets_map = {}
        sla_domain_map = {}
        def _generate_key(ticket):
            fields_list = self._sla_reset_trigger()
            key = list()
            for field_name in fields_list:
                if ticket._fields[field_name].type == 'many2one':
                    key.append(ticket[field_name].id)
                else:
                    key.append(ticket[field_name])
            return tuple(key)

        for ticket in self:
            if ticket.team_id.use_sla:  # limit to the team using SLA
                key = _generate_key(ticket)
                # group the ticket per key
                tickets_map.setdefault(key, self.env['helpdesk.ticket'])
                tickets_map[key] |= ticket
                # group the SLA to apply, by key
                if key not in sla_domain_map:
                    #sla_domain_map[key] = [('team_id', '=', ticket.team_id.id), ('priority', '<=', ticket.priority), ('stage_id.sequence', '>=', ticket.stage_id.sequence), '|', ('ticket_type_id', '=', ticket.ticket_type_id.id), ('ticket_type_id', '=', False)]
                    sla_domain_map[key] = [ ('ticket_type_id', '=', ticket.ticket_type_id.id)]  
                    
                    if ticket.team_id.name == 'MESA DE AYUDA SEGURIDAD':
                        sla_domain_map[key].append(('activity_id.subservice_id','=',ticket.subservice_id.id))
                    elif ticket.team_id.name == 'MESA DE AYUDA TECNOLOG??A':
                        sla_domain_map[key].append(('activity_id','=',ticket.activity_id.id))
                    

        result = {}
        for key, tickets in tickets_map.items():  # only one search per ticket group
            domain = sla_domain_map[key]
            result[tickets] = self.env['helpdesk.sla'].search(domain)  # SLA to apply on ticket subset

        return result
    
    @api.onchange('ans_datetime')
    def _onchange_ans_datetime(self):
        for record in self:
            if record.ans_datetime:
                record.sla_deadline = record.ans_datetime
                
    @api.onchange('service_id')
    def _onchange_subservices(self):
        ids=[]
        for record in self:
            record.subservice_id=False
            record.activity_id=False    
            if record.service_id.user_id and record.team_id.name == 'MESA DE AYUDA SEGURIDAD':
                record.user_id = record.service_id.user_id
            else:
                record.user_id = False
                
        if self.service_id:
            for subservice in self.service_id.subservice_ids:
                 for groups_id in subservice.group_users_id:
                    if self.env.user.id in groups_id.user_id.ids:
                        ids.append(subservice.id)
        return {'domain':{'subservice_id':[('id','in',ids)]}}
    
    ####################FILTRO PARA ACTIVIDADDES SEGUN SUBSERVICIO,TIPO TICKET Y USUARIOS ####################
    @api.onchange('subservice_id','ticket_type')
    def _onchange_activity_id(self):
        activity_obj = self.env['helpdesk.activity'].search([('subservice_id','=',self.subservice_id.id),('ticket_type','=',self.ticket_type)])
        ids= []
        for activity_id in activity_obj:
            self.activity_id = False
            if self.env.user.id in activity_id.users_ids.ids:
                ids.append(activity_id.id)
            
        return {'domain':{'activity_id':[('id','in',ids)]}}


###################################USUARIOS ASIGNADO A ############################################
    @api.onchange('group_users_id','activity_id')
    def _onchange_dominio_users(self):
        users_ids=[]
        if self.activity_id.users_id:
            self.user_id = self.activity_id.users_id.id
        else:
            self.user_id = False
        """
        if self.group_users_id:
            for group in self.group_users_id:
                users_ids += group.user_id.ids
        return {'domain':{'user_id':[('id','in',users_ids)]}}
        """
    @api.onchange('activity_id')
    def _onchange_dominio_groups(self):
        if self.activity_id:
            self.group_users_id=self.activity_id.group_users_id.id
            
    @api.onchange('ans_datetime')
    def _onchange_sla_deadline_manual(self):
        if self.ans_datetime:
            self.sla_deadline = self.ans_datetime
    
    @api.onchange('team_id')
    def _onchange_team_id(self):
        service_obj = self.env['helpdesk.service'].search([('team_id','=',self.team_id.id)])
        ids= []
        for service_id in service_obj:
            for groups_id in service_id.group_users_id:
                if self.env.user.id in groups_id.user_id.ids:
                    ids.append(service_id.id)
            
        return {'domain':{'service_id':[('id','in',ids)]}}
    

    @api.depends('stage_id')
    def _get_state_label(self):
        for record in self:
            if record.stage_id:
                record.state_record=(record.stage_id.name).upper()
            else:
                 record.state_record=False

    
    @api.depends('analisis_realizado')
    def _get_cargo_label(self):
        for record in self:
            if record.analisis_realizado:
                record.cargo=record.analisis_realizado.job_title
            else:
                 record.cargo=False
                    
    @api.depends('analisis_realizado_preprensa')
    def _get_cargo_label_preprensa(self):
        for record in self:
            if record.analisis_realizado_preprensa:
                record.cargo_preprensa=record.analisis_realizado_preprensa.job_title
            else:
                 record.cargo_preprensa=False
                    
    @api.depends('analisis_realizado_laboratorio')
    def _get_cargo_label_laboratorio(self):
        for record in self:
            if record.analisis_realizado_laboratorio:
                record.cargo_laboratorio=record.analisis_realizado_laboratorio.job_title
            else:
                 record.cargo_laboratorio=False

    @api.depends('activity_id')
    def _get_department_user(self):
        for record in self:
            record.departament = record.env.user.department_id.name
            
    @api.depends('activity_id')
    def _get_check_ans_fecha(self):
        for record in self:
            if record.activity_id.asn_date == True:
                record.check_ans_fecha=True
            else:
                 record.check_ans_fecha=False

    @api.depends('stage_id')
    def _get_total_ans(self):
        for record in self:
            record.sum_no_ans = record.tiempo_3ra_aprobacion + record.tiempo_aprobada_cliente + record.tiempo_hora_finalizada
            record.tiempo_gestion_tecnologia = record.tiempo_1ra_aprobacion + record.tiempo_2da_aprobacion + record.tiempo_aprobada

    @api.depends('activity_id')
    def _get_check_file_document(self):
        for record in self:
            if record.activity_id.file_request == True:
                record.check_file_document = True
            else:
                record.check_file_document = False

    @api.depends('service_id') 
    def _get_label_service_id(self):
        for record in self:
            if record.service_id:
                record.service_id_label = record.service_id.name
            else:
                record.service_id_label = False
    
    @api.depends('subservice_id')
    def _get_label_subservice(self):
        for record in self:
            if record.subservice_id:
                record.sub_service_id_label = record.subservice_id.name
            else:
                record.sub_service_id_label = False


    @api.depends('team_id')
    def _get_team_label(self):
        for record in self:
            if record.team_id:
                record.team_label = record.team_id.name
            else:
                record.team_label = False
                
    ##### Crear nuevo ticket
    @api.model
    def create(self, vals):
        for record in self:
    ######################APROBACIONES ###########################################
            if record.service_id.name == 'ASEGURAMIENTO DE PRODUCTOS':
                if not record.material:
                    raise ValidationError("Se Debe registrar m??nimo un material")
                    
            if record.service_id.name == 'MUESTRAS':
                if not record.muestras_id:
                    raise ValidationError("Se Debe registrar m??nimo una muestra")
                    
            if record.service_id.name == 'ORDENES DE SALIDA':
                if not record.producto_articulo:
                    raise ValidationError("Se Debe registrar m??nimo un producto/art??culo")
            
            if record.ans_datetime:
                if record.ans_datetime <= fields.Datetime.now():
                    raise ValidationError("La fecha seleccionada debe ser mayor a la actual")

        res = super(HelpdeskTicket, self).create(vals)

        return res

    def write(self, vals):
    
        if 'stage_id' in vals:
            for record in self:
                if record.state_record == 'NUEVO':
                   calc = fields.Datetime.now() - record.date_aper
                   calc_segundos= calc.seconds + record.tiempo_1ra_aprobacion
                   record.tiempo_1ra_aprobacion = calc_segundos
##################################TIEMPOS ETAPAS TECNOLOG??A ##################################################
                if record.state_record == 'EN REVISI??N' and record.fecha_hora_2da_aprobacion:
                   calc = fields.Datetime.now() - record.fecha_hora_2da_aprobacion
                   calc_segundos= calc.seconds + record.tiempo_2da_aprobacion
                   record.tiempo_2da_aprobacion = calc_segundos

                if record.state_record == 'APROBACI??N SEGURINFO' and record.fecha_hora_3ra_aprobacion:
                   calc = fields.Datetime.now() - record.fecha_hora_3ra_aprobacion
                   calc_segundos= calc.seconds + record.tiempo_3ra_aprobacion
                   record.tiempo_3ra_aprobacion = calc_segundos

                if record.state_record == 'EN ESPERA DE INFORMACI??N USUARIO' and record.fecha_hora_aprobada_cliente:
                   calc = fields.Datetime.now() - record.fecha_hora_aprobada_cliente
                   calc_segundos= calc.seconds + record.tiempo_aprobada_cliente
                   record.tiempo_aprobada_cliente = calc_segundos

                if record.state_record == 'EN GESTI??N' and record.fecha_hora_aprobacion:
                   calc = fields.Datetime.now() - record.fecha_hora_aprobacion
                   calc_segundos= calc.seconds + record.tiempo_aprobada
                   record.tiempo_aprobada = calc_segundos
                                                            
                if record.state_record == 'ESCALADO A TERCEROS' and record.fecha_hora_finalizada:
                   calc = fields.Datetime.now() - record.fecha_hora_finalizada
                   calc_segundos = calc.seconds + record.tiempo_hora_finalizada
                   record.tiempo_hora_finalizada = calc_segundos  
#######################################TIEMPOS ETAPA SEGURIDAD
                if record.state_record == 'REVISI??N' and record.fecha_hora_2da_aprobacion_2:
                   calc = fields.Datetime.now() - record.fecha_hora_2da_aprobacion_2
                   calc_segundos= calc.seconds + record.tiempo_2da_aprobacion_2
                   record.tiempo_2da_aprobacion_2 = calc_segundos

                if record.state_record == 'VERIFICACI??N (SEGURIDAD. LABORATORIO)' and record.fecha_hora_3ra_aprobacion_2:
                   calc = fields.Datetime.now() - record.fecha_hora_3ra_aprobacion_2
                   calc_segundos= calc.seconds + record.tiempo_3ra_aprobacion_2
                   record.tiempo_3ra_aprobacion_2 = calc_segundos

                if record.state_record == 'AUTORIZACI??N O APROBACIONES (SOLICITANTE, SEGURINFO, SEGURIDAD, COMERCIAL, OPERACIONES, TGSC)' and record.fecha_hora_aprobada_cliente_2:
                   calc = fields.Datetime.now() - record.fecha_hora_aprobada_cliente_2
                   calc_segundos= calc.seconds + record.tiempo_aprobada_cliente_2
                   record.tiempo_aprobada_cliente_2 = calc_segundos

                if record.state_record == 'DEVOLUCI??N / DESTRUCCI??N / ENTREGA' and record.fecha_hora_aprobacion_2:
                   calc = fields.Datetime.now() - record.fecha_hora_aprobacion_2
                   calc_segundos= calc.seconds + record.tiempo_aprobada_2
                   record.tiempo_aprobada_2 = calc_segundos
                                                            
                if record.state_record == 'EN TERCERO' and record.fecha_hora_finalizada_2:
                   calc = fields.Datetime.now() - record.fecha_hora_finalizada_2
                   calc_segundos = calc.seconds + record.tiempo_hora_finalizada_2
                   record.tiempo_hora_finalizada_2 = calc_segundos 
###################################################################################################################
                if record.state_record == 'SOLUCIONADO' and record.fecha_hora_solucion:
                   calc = fields.Datetime.now() - record.fecha_hora_solucion
                   calc_segundos= calc.seconds + record.tiempo_hora_solucion
                   record.tiempo_hora_solucion = calc_segundos   

                if record.state_record == 'CERRADO':
                    raise ValidationError("No se puede cambiar el estado del ticket una vez se ha cerrado")

        res = super(HelpdeskTicket, self).write(vals)
        
        if self.ans_datetime:
            if self.ans_datetime < fields.Datetime.now():
                raise ValidationError("La fecha seleccionada debe ser mayor a la actual")

        if 'stage_id' in vals:

            for record in self:
#########################################MOMENTO INGRESO ETAPA NUEVO################################
                if record.state_record == 'NUEVO':
                    raise ValidationError("No se puede pasar al estado NUEVO")
##########################MOMENTOS ETAPAS TECNOLOG??A##########################################
                if record.state_record == 'EN REVISI??N':
                    record.fecha_hora_2da_aprobacion=fields.Datetime().now()

                if record.state_record == 'APROBACI??N SEGURINFO':
                    record.fecha_hora_3ra_aprobacion=fields.Datetime().now()

                if record.state_record == 'EN ESPERA DE INFORMACI??N USUARIO':
                    record.fecha_hora_aprobada_cliente=fields.Datetime().now()

                if record.state_record == 'EN GESTI??N':
                    record.fecha_hora_aprobacion=fields.Datetime().now()

                if record.state_record == 'ESCALADO A TERCEROS':
                    record.fecha_hora_finalizada = fields.Datetime().now()

##################################MOMENTOS ETAPAS DE SEGURIDAD########################################
                if record.state_record == 'REVISI??N':
                    record.fecha_hora_2da_aprobacion_2 =fields.Datetime().now()

                if record.state_record == 'VERIFICACI??N (SEGURIDAD. LABORATORIO)':
                    record.fecha_hora_3ra_aprobacion_2 =fields.Datetime().now()


                if record.state_record == 'AUTORIZACI??N O APROBACIONES (SOLICITANTE, SEGURINFO, SEGURIDAD, COMERCIAL, OPERACIONES, TGSC)':
                    record.fecha_hora_aprobada_cliente_2 =fields.Datetime().now()


                if record.state_record == 'DEVOLUCI??N / DESTRUCCI??N / ENTREGA':
                    record.fecha_hora_aprobacion_2 = fields.Datetime().now()


                if record.state_record == 'EN TERCERO':
                    record.fecha_hora_finalizada_2 =fields.Datetime().now()
######################################MOMENTO ENTRAR ETAPA SOLUCIONADO ################################
                    
                if record.state_record == 'SOLUCIONADO':
                    record.fecha_hora_solucion = fields.Datetime().now()


               # if record.state_record == 'CERRADO':
               #     raise ValidationError("Debe ser aprobado por el Jefe de departamento")

                  #  hourst, secondst = divmod(calct * 60, 3600)  # split to hours and seconds
                  #  minutest, secondst = divmod(secondst, 60)  # split the seconds to minutes and seconds
                  #  hours, seconds = divmod(calc * 60, 3600)  # split to hours and seconds
                  #  minutes, seconds = divmod(seconds, 60)  # split the seconds to minutes and seconds

    
        ####################################################APROBACIONES########################################
       # if self.service_id.name == 'ORDENES DE SALIDA' and  self.aprobado_jede_departamento != 'Si':
       #     if self.stage_id.name == 'AUTORIZACI??N O APROBACIONES (SOLICITANTE, SEGURINFO, SEGURIDAD, COMERCIAL, OPERACIONES, TGSC)':
       #         raise ValidationError("Debe ser aprobado por el Jefe de departamento")
                
       # if self.service_id.name == 'ORDENES DE SALIDA' and  self.aprobado_seguridad != 'Si':
       #     if self.stage_id.name == 'AUTORIZACI??N O APROBACIONES (SOLICITANTE, SEGURINFO, SEGURIDAD, COMERCIAL, OPERACIONES, TGSC)':
       #         raise ValidationError("Debe ser aprobado por el Jefe de seguridad")
                
       # if self.service_id.name == 'INFORME AN??LISIS DE AUTENTICIDAD' and  self.aprobado_gerencia_seguridad == False:
       #     if self.stage_id.name == 'DEVOLUCI??N / DESTRUCCI??N / ENTREGA':
       #         raise ValidationError("Debe ser aprobado por gerencia de seguridad")
                
       # if self.service_id.name == 'INGRESO COMPA????A VISITANTES' and  self.aprobado_salud == False:
       #     if self.stage_id.name == 'DEVOLUCI??N / DESTRUCCI??N / ENTREGA':
       #         raise ValidationError("Debe ser aprobado por Salud ocupacional")

      #  if self.service_id.name == 'MUESTRAS' and  self.aprobado_gerencia == False:
       #     if self.stage_id.name == 'DEVOLUCI??N / DESTRUCCI??N / ENTREGA':
       #         raise ValidationError("Debe ser aprobado por Gerencia")
        
                
       # if self.service_id.name == 'MUESTRAS' and  self.aprobado_gerencia_seguridad == False:
       #     if self.stage_id.name == 'DEVOLUCI??N / DESTRUCCI??N / ENTREGA':
       #         raise ValidationError("Debe ser aprobado por Gerencia de Seguridad")
    
        if self.service_id.name == 'ASEGURAMIENTO DE PRODUCTOS':
            if not self.material:
                raise ValidationError("Se Debe registrar un material")
                
        if self.service_id.name == 'MUESTRAS':
                if not self.muestras_id:
                    raise ValidationError("Se Debe registrar m??nimo una muestra")

                
        if self.service_id.name == 'ORDENES DE SALIDA':
                if not self.producto_articulo:
                    raise ValidationError("Se Debe registrar m??nimo un producto/art??culo")
        
        if self.team_id.name == 'MESA DE AYUDA TECNOLOG??A':
            if self.stage_id.name != 'NUEVO':
                if self.stage_id.name != 'EN REVISI??N':
                    if not self.required_information_ticket:
                        raise ValidationError("Seleccione una opci??n en 'Informaci??n requerida en el ticket esta completa'")
       #             if not self.info_security_scale:
      #                  raise ValidationError("Seleccione una opci??n en 'Ticket requiere de seguridad de la informaci??n'")

                    
        return res
    
    ##########################################TIEMPO TTOTAL DEL TICKET################################
    @api.depends('create_date', 'close_date')
    def _compute_close_hours(self):
        for ticket in self:
            create_date = fields.Datetime.from_string(ticket.create_date)
            if create_date and ticket.close_date:
                duration_data = ticket.team_id.resource_calendar_id.get_work_duration_data(create_date, fields.Datetime.from_string(ticket.close_date), compute_leaves=True)
                ticket.close_hours = duration_data['hours']*3600
            else:
                ticket.close_hours = False
    
    def action_stage_next(self):
        for record in self:
            if record.team_label == 'MESA DE AYUDA TECNOLOG??A':
                if record.stage_id.name == 'NUEVO':
                    ticket_sudo = self.env['helpdesk.stage'].search([('name','=','EN REVISI??N')])
                    record.write({'stage_id':ticket_sudo.id})
                elif record.stage_id.name == 'EN REVISI??N':
                    ticket_sudo = self.env['helpdesk.stage'].search([('name','=','APROBACI??N SEGURINFO')])
                    record.write({'stage_id':ticket_sudo.id})
                elif record.stage_id.name == 'APROBACI??N SEGURINFO':
                    ticket_sudo = self.env['helpdesk.stage'].search([('name','=','EN ESPERA DE INFORMACI??N USUARIO')])
                    record.write({'stage_id':ticket_sudo.id})
                elif record.stage_id.name == 'EN ESPERA DE INFORMACI??N USUARIO':
                    ticket_sudo = self.env['helpdesk.stage'].search([('name','=','EN GESTI??N')])
                    record.write({'stage_id':ticket_sudo.id})
                elif record.stage_id.name == 'EN GESTI??N':
                    ticket_sudo = self.env['helpdesk.stage'].search([('name','=','ESCALADO A TERCEROS')])
                    record.write({'stage_id':ticket_sudo.id})
                elif record.stage_id.name == 'ESCALADO A TERCEROS':
                    ticket_sudo = self.env['helpdesk.stage'].search([('name','=','SOLUCIONADO')])
                    record.write({'stage_id':ticket_sudo.id})
                elif record.stage_id.name == 'SOLUCIONADO':
                    ticket_sudo = self.env['helpdesk.stage'].search([('name','=','CERRADO')])
                    record.write({'stage_id':ticket_sudo.id})

            else:
                if record.stage_id.name == 'REVISI??N':
                    ticket_sudo = self.env['helpdesk.stage'].search([('name','=','VERIFICACI??N (SEGURIDAD. LABORATORIO)')])
                    record.write({'stage_id':ticket_sudo.id})
                elif record.stage_id.name == 'VERIFICACI??N (SEGURIDAD. LABORATORIO)':
                    ticket_sudo = self.env['helpdesk.stage'].search([('name','=','AUTORIZACI??N O APROBACIONES (SOLICITANTE, SEGURINFO, SEGURIDAD, COMERCIAL, OPERACIONES, TGSC)')])
                    record.write({'stage_id':ticket_sudo.id})
                elif record.stage_id.name == 'AUTORIZACI??N O APROBACIONES (SOLICITANTE, SEGURINFO, SEGURIDAD, COMERCIAL, OPERACIONES, TGSC)':
                    ticket_sudo = self.env['helpdesk.stage'].search([('name','=','DEVOLUCI??N / DESTRUCCI??N / ENTREGA')])
                    record.write({'stage_id':ticket_sudo.id})
                elif record.stage_id.name == 'DEVOLUCI??N / DESTRUCCI??N / ENTREGA':
                    ticket_sudo = self.env['helpdesk.stage'].search([('name','=','EN TERCERO')])
                    record.write({'stage_id':ticket_sudo.id})
                elif record.stage_id.name == 'EN TERCERO':
                    ticket_sudo = self.env['helpdesk.stage'].search([('name','=','SOLUCIONADO')])
                    record.write({'stage_id':ticket_sudo.id})
                elif record.stage_id.name == 'SOLUCIONADO':
                    ticket_sudo = self.env['helpdesk.stage'].search([('name','=','CERRADO')])
                    record.write({'stage_id':ticket_sudo.id})
                    
    def action_stage_return(self):
        for record in self:
            if record.team_label == 'MESA DE AYUDA TECNOLOG??A':
                if record.stage_id.name == 'EN REVISI??N': 
                    ticket_sudo = self.env['helpdesk.stage'].search([('name','=','NUEVO')])
                    record.write({'stage_id':ticket_sudo.id})
                elif record.stage_id.name == 'APROBACI??N SEGURINFO':  
                    ticket_sudo = self.env['helpdesk.stage'].search([('name','=','EN REVISI??N')])
                    record.write({'stage_id':ticket_sudo.id})
                elif record.stage_id.name == 'EN ESPERA DE INFORMACI??N USUARIO':  
                    ticket_sudo = self.env['helpdesk.stage'].search([('name','=','APROBACI??N SEGURINFO')])
                    record.write({'stage_id':ticket_sudo.id}) 
                elif record.stage_id.name == 'EN GESTI??N':   
                    ticket_sudo = self.env['helpdesk.stage'].search([('name','=','EN ESPERA DE INFORMACI??N USUARIO')])
                    record.write({'stage_id':ticket_sudo.id})
                elif record.stage_id.name == 'ESCALADO A TERCEROS': 
                    ticket_sudo = self.env['helpdesk.stage'].search([('name','=','EN GESTI??N')])
                    record.write({'stage_id':ticket_sudo.id})
                elif record.stage_id.name == 'SOLUCIONADO': 
                    ticket_sudo = self.env['helpdesk.stage'].search([('name','=','ESCALADO A TERCEROS')])
                    record.write({'stage_id':ticket_sudo.id})
                elif record.stage_id.name == 'CERRADO':
                    ticket_sudo = self.env['helpdesk.stage'].search([('name','=','SOLUCIONADO')])
                    record.write({'stage_id':ticket_sudo.id})

            else:
                if record.stage_id.name == 'VERIFICACI??N (SEGURIDAD. LABORATORIO)': 
                    ticket_sudo = self.env['helpdesk.stage'].search([('name','=','REVISI??N')])
                    record.write({'stage_id':ticket_sudo.id})
                elif record.stage_id.name == 'AUTORIZACI??N O APROBACIONES (SOLICITANTE, SEGURINFO, SEGURIDAD, COMERCIAL, OPERACIONES, TGSC)': 
                    ticket_sudo = self.env['helpdesk.stage'].search([('name','=','VERIFICACI??N (SEGURIDAD. LABORATORIO)')])
                    record.write({'stage_id':ticket_sudo.id})
                elif record.stage_id.name == 'DEVOLUCI??N / DESTRUCCI??N / ENTREGA':
                    ticket_sudo = self.env['helpdesk.stage'].search([('name','=','AUTORIZACI??N O APROBACIONES (SOLICITANTE, SEGURINFO, SEGURIDAD, COMERCIAL, OPERACIONES, TGSC)')])
                    record.write({'stage_id':ticket_sudo.id})
                elif record.stage_id.name == 'EN TERCERO':
                    ticket_sudo = self.env['helpdesk.stage'].search([('name','=','DEVOLUCI??N / DESTRUCCI??N / ENTREGA')])
                    record.write({'stage_id':ticket_sudo.id})
                elif record.stage_id.name == 'SOLUCIONADO':
                    ticket_sudo = self.env['helpdesk.stage'].search([('name','=','EN TERCERO')])
                    record.write({'stage_id':ticket_sudo.id})
                elif record.stage_id.name == 'CERRADO':
                    ticket_sudo = self.env['helpdesk.stage'].search([('name','=','SOLUCIONADO')])
                    record.write({'stage_id':ticket_sudo.id})
                    

    def action_stage_cancel(self):
        for record in self:
            if record.team_label == 'MESA DE AYUDA TECNOLOG??A':
                ticket_sudo = self.env['helpdesk.stage'].search([('name','=','CANCELADO')])
                record.write({'stage_id':ticket_sudo.id})
            elif record.team_label == 'MESA DE AYUDA SEGURIDAD':
                ticket_sudo = self.env['helpdesk.stage'].search([('name','=','RECHAZADO')])
                record.write({'stage_id':ticket_sudo.id})
                
    ####################EXPORTAR FLOTANTE EN FORMATO HORAS#######################################
    def float_time_convert(self, float_val):
        factor = float_val < 0 and -1 or 1
        val = abs(float_val)
        return (factor * int(math.floor(val)), int(round((val % 1) * 60)))

    def export_data(self, fields_to_export):
        """ Override to fix hour format in export file """
        res = super(HelpdeskTicket, self).export_data(fields_to_export)
        index = range(len(fields_to_export))
        fields_name = dict(zip(fields_to_export,index))
        try:
            for index, val in enumerate(res['datas']):

                if fields_name.get('sum_no_ans'):
                    fieldindex = fields_name.get('sum_no_ans')
                    sum_no_ans = float(res['datas'][index][fieldindex])
                    seconds = sum_no_ans
                    minutes = seconds / 60
                    hours = minutes / 60
                    res['datas'][index][fieldindex] = "%02d:%02d:%02d" % (hours, minutes % 60, seconds % 60)
                if fields_name.get('tiempo_gestion_tecnologia'):
                    fieldindex = fields_name.get('tiempo_gestion_tecnologia')
                    tiempo_gestion_tecnologia = float(res['datas'][index][fieldindex])
                    seconds = tiempo_gestion_tecnologia
                    minutes = seconds / 60
                    hours = minutes / 60
                    res['datas'][index][fieldindex] = "%02d:%02d:%02d" % (hours, minutes % 60, seconds % 60)
                if fields_name.get('tiempo_1ra_aprobacion'):
                    fieldindex = fields_name.get('tiempo_1ra_aprobacion')
                    tiempo_1ra_aprobacion = float(res['datas'][index][fieldindex])
                    seconds = tiempo_1ra_aprobacion
                    minutes = seconds / 60
                    hours = minutes / 60

                    res['datas'][index][fieldindex] = "%02d:%02d:%02d" % (hours, minutes % 60, seconds % 60)
                if fields_name.get('tiempo_2da_aprobacion'):
                    fieldindex = fields_name.get('tiempo_2da_aprobacion')
                    tiempo_2da_aprobacion = float(res['datas'][index][fieldindex])
                    seconds = tiempo_2da_aprobacion
                    minutes = seconds / 60
                    hours = minutes / 60
                    res['datas'][index][fieldindex] = "%02d:%02d:%02d" % (hours, minutes % 60, seconds % 60)
                if fields_name.get('tiempo_3ra_aprobacion'):
                    fieldindex = fields_name.get('tiempo_3ra_aprobacion')
                    tiempo_3ra_aprobacion = float(res['datas'][index][fieldindex])
                    seconds = tiempo_3ra_aprobacion
                    minutes = seconds / 60
                    hours = minutes / 60
                    res['datas'][index][fieldindex] = "%02d:%02d:%02d" % (hours, minutes % 60, seconds % 60)
                if fields_name.get('tiempo_aprobada_cliente'):
                    fieldindex = fields_name.get('tiempo_aprobada_cliente')
                    tiempo_aprobada_cliente = float(res['datas'][index][fieldindex])
                    seconds = tiempo_aprobada_cliente
                    minutes = seconds / 60
                    hours = minutes / 60
                    res['datas'][index][fieldindex] = "%02d:%02d:%02d" % (hours, minutes % 60, seconds % 60)
                if fields_name.get('tiempo_1ra_aprobacion_2'):
                    fieldindex = fields_name.get('tiempo_1ra_aprobacion_2')
                    tiempo_1ra_aprobacion_2 = float(res['datas'][index][fieldindex])
                    seconds = tiempo_1ra_aprobacion_2
                    minutes = seconds / 60
                    hours = minutes / 60

                    res['datas'][index][fieldindex] = "%02d:%02d:%02d" % (hours, minutes % 60, seconds % 60)
                if fields_name.get('tiempo_2da_aprobacion_2'):
                    fieldindex = fields_name.get('tiempo_2da_aprobacion_2')
                    tiempo_2da_aprobacion_2 = float(res['datas'][index][fieldindex])
                    seconds = tiempo_2da_aprobacion_2
                    minutes = seconds / 60
                    hours = minutes / 60
                    res['datas'][index][fieldindex] = "%02d:%02d:%02d" % (hours, minutes % 60, seconds % 60)
                if fields_name.get('tiempo_3ra_aprobacion_2'):
                    fieldindex = fields_name.get('tiempo_3ra_aprobacion_2')
                    tiempo_3ra_aprobacion_2 = float(res['datas'][index][fieldindex])
                    seconds = tiempo_3ra_aprobacion_2
                    minutes = seconds / 60
                    hours = minutes / 60
                    res['datas'][index][fieldindex] = "%02d:%02d:%02d" % (hours, minutes % 60, seconds % 60)
                if fields_name.get('tiempo_aprobada_cliente_2'):
                    fieldindex = fields_name.get('tiempo_aprobada_cliente_2')
                    tiempo_aprobada_cliente_2 = float(res['datas'][index][fieldindex])
                    seconds = tiempo_aprobada_cliente_2
                    minutes = seconds / 60
                    hours = minutes / 60
                    res['datas'][index][fieldindex] = "%02d:%02d:%02d" % (hours, minutes % 60, seconds % 60)
                if fields_name.get('tiempo_aprobada_2'):
                    fieldindex = fields_name.get('tiempo_aprobada_2')
                    tiempo_aprobada_2 = float(res['datas'][index][fieldindex])
                    seconds = tiempo_aprobada_2
                    minutes = seconds / 60
                    hours = minutes / 60
                    res['datas'][index][fieldindex] = "%02d:%02d:%02d" % (hours, minutes % 60, seconds % 60)
                if fields_name.get('tiempo_hora_finalizada'):
                    fieldindex = fields_name.get('tiempo_hora_finalizada')
                    tiempo_hora_finalizada = float(res['datas'][index][fieldindex])
                    seconds = tiempo_hora_finalizada
                    minutes = seconds / 60
                    hours = minutes / 60
                    res['datas'][index][fieldindex] = "%02d:%02d:%02d" % (hours, minutes % 60, seconds % 60)
                if fields_name.get('tiempo_hora_solucion'):
                    fieldindex = fields_name.get('tiempo_hora_solucion')
                    tiempo_hora_solucion = float(res['datas'][index][fieldindex])
                    seconds = tiempo_hora_solucion
                    minutes = seconds / 60
                    hours = minutes / 60
                    res['datas'][index][fieldindex] = "%02d:%02d:%02d" % (hours, minutes % 60, seconds % 60)
        except Exception as e:
            raise ValidationError('It was not possible to convert the time format when exporting the file.')
        return res

    @api.depends('sla_status_ids.deadline', 'sla_status_ids.reached_datetime','ans_datetime')
    def _compute_sla_deadline(self):
        """ Keep the deadline for the last stage (closed one), so a closed ticket can have a status failed.
            Note: a ticket in a closed stage will probably have no deadline
        """
        for ticket in self:
            if self.ans_datetime:
                self.sla_deadline = self.ans_datetime
            else:
                deadline = self.sla_deadline
                status_not_reached = ticket.sla_status_ids.filtered(lambda status: not status.reached_datetime)
                ticket.sla_deadline = min(status_not_reached.mapped('deadline')) if status_not_reached else deadline
                
                
                
    #########################TABLAS DE CORREO##############################
    
    
    def get_table_muestras(self):
        '''
        <table>
            <tr>
                <th>Nombre</th>
            </tr>
            <tr>
                <td>Nombre 1</td>
            </tr>
            <tr>
                <td>Nombre 2</td>
            </tr>
        </table> 
        '''
        table = ''
        table += ''' 
            <table border="1">
                <tr>
                    <th>Nombre</th>
                    <th>Cliente</th>
                    <th>Cantidad</th>
                    <th>SET</th>
                    <th>Orden de Producci??n</th>
                </tr>
        '''
        flag = False
        for  muestras in self.muestras_id:
            flag = True
            table += '<tr>'
            table += '<td>' + muestras.name + '      </td>'
            table += '<td>' + muestras.cliente + '      </td>'
            table += '<td>' + str(muestras.cantidad) + '     </td>'
            table += '<td>' + str(muestras.sett) + '     </td>'
            table += '<td>' + muestras.orden_produccion + '     </td>'
            table += '</tr>'
        table += ''' 
            </table> 
        '''
        return table if flag else False

    def get_table_material(self):
        '''
        <table>
            <tr>
                <th>Nombre</th>
            </tr>
            <tr>
                <td>Nombre 1</td>
            </tr>
            <tr>
                <td>Nombre 2</td>
            </tr>
        </table> 
        '''
        table = ''
        table += ''' 
            <table border="1">
                <tr>
                    <th>Nombre</th>
                    <th>Cantidad</th>
                    <th>Cliente</th>
                    <th>Unidad de Medida</th>
                </tr>
        '''
        flag = False
        for  mat in self.material:
            flag = True
            table += '<tr>'
            table += '<td>' + mat.name + '      </td>'
            table += '<td>' + str(mat.cantidad) + '      </td>'
            table += '<td>' + mat.cliente + '     </td>'
            table += '<td>' + mat.unidad + '     </td>'
            table += '</tr>'
        table += ''' 
            </table> 
        '''
        return table if flag else False

    def get_table_producto_articulo(self):
        '''
        <table>
            <tr>
                <th>Nombre</th>
            </tr>
            <tr>
                <td>Nombre 1</td>
            </tr>
            <tr>
                <td>Nombre 2</td>
            </tr>
        </table> 
        '''
        table = ''
        table += ''' 
            <table border="1">
                <tr>
                    <th>Nombre</th>
                    <th>Unidad de Medida</th>
                    <th>Cantidad</th>
                </tr>
        '''
        flag = False
        for  producto in self.producto_articulo:
            flag = True
            table += '<tr>'
            table += '<td>' + producto.name + '      </td>'
            table += '<td>' + producto.unidad + '      </td>'
            table += '<td>' + str(producto.cantidad) + '     </td>'
            table += '</tr>'
        table += ''' 
            </table> 
        '''
        return table if flag else False


    def get_table_registro_personas(self):
        '''
        <table>
            <tr>
                <th>Nombre</th>
            </tr>
            <tr>
                <td>Nombre 1</td>
            </tr>
            <tr>
                <td>Nombre 2</td>
            </tr>
        </table> 
        '''
        table = ''
        table += ''' 
            <table border="1">
                <tr>
                    <th>Nombre</th>
                    <th>C??dula</th>
                    <th>Serial Equipo</th>
                    <th>Empresa</th>
                    <th>Arl</th>
                    <th>Eps</th>
                </tr>
        '''
        flag = False

        if self.area_ingreso == 'administrativa':
            registro=self.registro_personas
        else:
            registro=self.registro_personas_adjunto

        for reg_per in registro:
            flag = True
            table += '<tr>'
            table += '<td>' + reg_per.name + ' </td>'
            table += '<td>' + str(reg_per.cedula) + '</td>'
            table += '<td>' + reg_per.serial_equipo + '</td>'
            table += '<td>' + reg_per.empresa + '</td>'
            table += '<td>' + reg_per.arl + '</td>'
            table += '<td>' + reg_per.eps + '</td>'
            table += '</tr>'
        table += ''' 
            </table> 
        '''
        return table if flag else False
