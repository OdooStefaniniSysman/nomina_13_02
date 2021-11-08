#Todoo SAS

from odoo import models, fields, api

class QualityCheck(models.Model):
    _inherit = 'quality.check'

    workcenter_mpr_id = fields.Many2one('mrp.workcenter', string="Centro de Producción", tracking=True)
    sale_order_id = fields.Many2one('sale.order', string="Orden de Venta", tracking=True)
    client = fields.Many2one(string="Cliente", related="sale_order_id.partner_id", tracking=True)
    turn_type = fields.Selection([('mañana','Mañana'),('tarde','Tarde'),('noche','Noche')], string="Turno", tracking=True )
    presser_id = fields.Many2one('quality.presser', string="Prensista", tracking=True)
    user_id_admin = fields.Many2one('res.users', string="Responsable")
    type_find = fields.Many2one('quality.type.find', string="Tipo de Hallazgo", tracking=True)
    process = fields.Many2one('quality.process', string="Proceso", tracking=True)
    not_compliant = fields.Boolean(string="No Conforme", tracking=True)
    consecutive = fields.Char(string="Consecutivo No conforme", tracking=True, copy="False")
    consecutive_mp = fields.Char(string="Consecutivo No conforme", tracking=True, copy="False")
    consecutive_product_progress = fields.Char(string="Consecutivo No conforme", tracking=True, copy="False")
    consecutive_validation = fields.Char(string="Consecutivo No conforme", tracking=True, copy="False")
    not_conformity_type = fields.Selection([('mp','No Conformidad Materia Prima'),('pt','No Conformidad Producto Terminado')], string="Tipo de no conformidad")
    identification_type = fields.Selection([('inspeccion','Identificada en Inspección'),('proceso','Identificada en Proceso')], string="Tipo de Identificación")
    purchase_order_id = fields.Many2one('purchase.order', string="Orden de Compra")
    partner_id = fields.Many2one('res.partner', string="Proveedor")
    quantity_po = fields.Float(string="Cantidad")
    description_not_conformity = fields.Text(string="Descripción de la No Conformidad", tracking=True)
    evaluation_results = fields.Text(string="Resultados de la evaluación", tracking=True)
    material_arrangement_type = fields.Selection([('reprocesado','Reprocesado'),('rechazado','Rechazado'),('reclasificado','Reclasificado'),('aceptado','Aceptado por Degoración con Reparación'),('aceptadocr','Aceptado por Degoración sin Reparación')], string="Disposición de material no conforme")
    disposition_comments = fields.Text(string="Comentarios sobre la disposición", tracking=True)
    user_id_responsable = fields.Many2one('res.users', string="Responsable de la disposición", tracking=True)
    user_id_validator = fields.Many2one('res.users', string="Responsable de Liberación", tracking=True)
    user_id_responsable_th = fields.Many2one('res.users', string="Responsable", tracking=True)
    datetime = fields.Datetime(string="Fecha y Hora", tracking=True)
    check = fields.Boolean(string="Verificar", compute="_compute_check_team_id")
    supplier_rating = fields.Char(string="Calificación del Proveedor", tracking=True)
    quality_certificate = fields.Char(string="Certificado de Calidad", tracking=True)
    acceptance_number = fields.Char(string="Número de Aceptación", tracking=True)
    rejection_number = fields.Char(string="Número de Rechazo", tracking=True)
    sampling_datetime = fields.Datetime(string="Fecha y hora de Muestreo", tracking=True)
    total_quantity = fields.Float(string="Cantidad Total Recibida", related="picking_id.move_ids_without_package.product_uom_qty", tracking=True)
    inspection_type_nivel = fields.Char(string="Tipo/Nivel de Inspección",tracking=True)
    key_letter = fields.Char(string="Letra Clave", tracking=True)
    make_quantity = fields.Float(string="Cantidad Muestra Tomada")
    approver = fields.Selection([('si','Si'),('no','No')], string="Aprobado")
    check_mp = fields.Boolean(string="Check Inspeción de Materias Primas", compute="_compute_check_mp")
    date_done = fields.Datetime(string="Fecha y Hora de Recepción")
    partner_id_not_conformity_product = fields.Many2one('res.partner', string="Cliente")
    production_order_id = fields.Many2one('mrp.production', string="Orden de Producción")
    production_order_id_th = fields.Many2one('mrp.production', string="Orden de Producción")
    unit_of_mesure = fields.Char(string="Unidad de Medida")
    quantity_not_conformity_product = fields.Float(string="Cantidad")
    product_text = fields.Char(string="Producto Homólogo")
    reception_date = fields.Datetime(string="Fecha y Hora de Recepción")
    check_new_mp = fields.Boolean(string="Check Nuevas materias primas e insumos", compute="_compute_check_newmp")
    check_mp_not_conformity = fields.Boolean(string="Check Manejo de MP no conforme identificada en proceso", compute="_compute_check_mp_not_conformity")
    priority = fields.Selection([
        ('0', 'Normal'),
        ('1', 'Important'),
        ('2', 'High'),
        ('3', 'Very High'),
    ], index=True, string="Prioridad")

    
    @api.depends('team_id')
    def _compute_check_team_id(self):
        for record in self:
            record.check = True if record.team_id and record.team_id[0].name  == 'Inspección de producto en proceso' else False


    @api.depends('team_id')
    def _compute_check_mp(self):
        for record in self:
            record.check_mp = True if record.team_id and record.team_id[0].name  == 'Inspección de Materias Primas' else False

    
    @api.depends('team_id')
    def _compute_check_newmp(self):
        for record in self:
            record.check_new_mp = True if record.team_id and record.team_id[0].name  == 'Validación nuevas materias primas e insumos' else False

    @api.depends('team_id')
    def _compute_check_mp_not_conformity(self):
        for record in self:
            record.check_mp_not_conformity = True if record.team_id and record.team_id[0].name  == 'Manejo de MP no conforme identificada en proceso' else False                             
