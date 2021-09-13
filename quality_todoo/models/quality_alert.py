#Luis Felipe Paternina
#Ingeniero de Sistemas
#Todoo SAS
from odoo import models, fields, api

class QualityAlert(models.Model):
    _inherit = 'quality.alert'

    not_compliant = fields.Boolean(string="No Conforme", tracking=True)
    approved_type = fields.Selection([('si','Si'),('no','No')],string="Aprobado", tracking=True)
    sampling_datetime = fields.Datetime(string="Fecha y hora de Muestreo", tracking=True)
    total_quantity = fields.Float(string="Cantidad Total Recibida", tracking=True)
    level_inspection = fields.Char(string="Tipo / Nivel de Inspección", tracking=True)
    key_letter = fields.Char(string="Letra Clave", tracking=True)
    amount_of_letter = fields.Float(string="Cantidad Muestra Tomada", tracking=True)
    reception_datetime = fields.Datetime(string="Fecha y Hora de Recepción", tracking=True)
    supplier_rating = fields.Char(string="Calificación del Proveedor", tracking=True)
    quality_certificate = fields.Char(string="Certificado de Calidad", tracking=True)
    acceptance_number = fields.Char(string="Número de Aceptación", tracking=True)
    rejection_number = fields.Char(string="Número de Rechazo", tracking=True)
    not_conformity_type = fields.Selection([('mp','No Conformidad Materia Prima'),('pt','No Conformidad Producto Terminado')], string="Tipo de no conformidad")
    consecutive = fields.Char(string="Consecutivo No conforme", tracking=True, copy="False")
    user_id_admin = fields.Many2one('res.users', string="Responsable de Liberación")
    identification_type = fields.Selection([('inspeccion','Identificada en Inspección'),('proceso','Identificada en Proceso')], string="Tipo de Identificación")
    purchase_order_id = fields.Many2one('purchase.order', string="Orden de Compra")
    partner_id = fields.Many2one('res.partner', string="Proveedor")
    quantity_po = fields.Float(string="Cantidad")
    description_not_conformity = fields.Text(string="Descripción de la No Conformidad", tracking=True)
    evaluation_results = fields.Text(string="Resultados de la evaluación", tracking=True)
    material_arrangement_type = fields.Selection([('reprocesado','Reprocesado'),('rechazado','Rechazado'),('reclasificado','Reclasificado'),('aceptado','Aceptado por Degoración con Reparación'),('aceptadocr','Aceptado por Degoración sin Reparación')], string="Disposición de material no conforme")
    disposition_comments = fields.Text(string="Comentarios sobre la disposición", tracking=True)
    user_id_responsable = fields.Many2one('res.users', string="Responsable de la disposición", tracking=True)
    workcenter_mpr_id = fields.Many2one('mrp.workcenter', string="Centro de Producción", tracking=True)
    client = fields.Char(string="Cliente", tracking=True)
    turn_type = fields.Selection([('mañana','Mañana'),('tarde','Tarde'),('noche','Noche')], string="Turno", tracking=True )
    contract_id = fields.Many2one('quality.presser', string="Prensista", tracking=True)
    process = fields.Many2one('quality.process', string="Proceso", tracking=True)
    type_find = fields.Many2one('quality.type.find', string="Tipo de Hallazgo", tracking=True)
    check = fields.Boolean(string="Verificar", compute='_compute_check_tag_ids')
    sale_order_id = fields.Many2one('sale.order', string="Orden de Venta", tracking=True)
    purchase_order_material_id = fields.Many2one('purchase.order', string="Orden de Compra")
    check_material = fields.Boolean(string="Verificar Materias Primas", compute='_compute_check_material')
    programing_date_datetime = fields.Datetime(string="Fecha y hora de Programación")
    check_handle_mp = fields.Boolean(string="Verificar Manejo MP", compute='_compute_check_handle_mp')
    check_inspection = fields.Boolean(string="Verificar Inspección", compute="_compute_check_inspection")
    production_order_id = fields.Many2one('mrp.production', string="Orden de Producción")
    product_text = fields.Char(string="Producto Homólogo")
    partner_id_not_conformity_product = fields.Many2one('res.partner', string="Cliente")
    production_order_id = fields.Many2one('mrp.production', string="Orden de Producción")
    quantity_not_conformity_product = fields.Float(string="Cantidad")
    picking_id = fields.Many2one('stock.picking', string="Picking")
    unit_of_mesure = fields.Char(string="Unidad de Medida")
    unit_of_mesure_po = fields.Char(string="Unidad de Medida")
    approver = fields.Selection([('si','Si'),('no','No')], string="Aprobado")
    datetime_alert = fields.Datetime(string="Fecha y Hora")

   
    @api.depends('team_id')
    def _compute_check_tag_ids(self):
        for record in self:
            record.check = True if record.team_id and record.team_id[0].name  == 'Inspección de producto en proceso' else False

    @api.depends('team_id')
    def _compute_check_material(self):
        for record in self:
            record.check_material = True if record.team_id and record.team_id[0].name  == 'Validación nuevas materias primas e insumos' else False

    @api.depends('team_id')
    def _compute_check_handle_mp(self):
        for record in self:
            record.check_handle_mp = True if record.team_id and record.team_id[0].name  == 'Manejo de MP no conforme identificada en proceso' else False

    @api.depends('team_id')
    def _compute_check_inspection(self):
        for record in self:
            record.check_inspection = True if record.team_id and record.team_id[0].name  == 'Inspección de Materias Primas' else False                          	