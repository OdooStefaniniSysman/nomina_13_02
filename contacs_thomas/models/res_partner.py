# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime,date,timedelta


class AdressContact(models.Model):
    _name = 'adress.contact'

    name = fields.Char('Model: adress')


class StreetCode(models.Model):
    _name = 'street.code'

    name = fields.Char('Descripción')
    code = fields.Char('Código')
    company_id = fields.Many2one('res.company')


class AdressCode(models.Model):
    _name = 'address.code'

    name = fields.Char('Descripción')
    code = fields.Char('Código')
    company_id = fields.Many2one('res.company')


class CiiuValue(models.Model):
    _name = 'ciiu.value'

    name = fields.Char('Descripción')
    code = fields.Char('Código')
    company_id = fields.Many2one('res.company')


class ResIndicativeState(models.Model):
    _inherit = 'res.country.state'

    indicative_state_code = fields.Integer(string="Indicativo de provincia")


class ResPartner(models.Model):
    _inherit = 'res.partner'

    # constraint is commented because it does not apply to business rules
    #_sql_constraints = [
    #    ('doc_unique',
         #'UNIQUE(l10n_co_document_type,vat,company_id,company_type)',
    #     'UNIQUE(vat)',
    #     "Ya existe un tercero con este mismo documento"),
    #]

     ################## GRUPO NOMBRE DE CLIENTE Y COMPAÑIA #####################3
    company_type = fields.Selection(tracking=True)
    company_name = fields.Char(tracking=True)

    firts_name = fields.Char('Nombre 1')
    last_name = fields.Char('Nombre 2')
    middle_name = fields.Char('Nombre 3')
    second_last_name = fields.Char('Nombre 4')
    company_nature = fields.Selection([('S.A.S.', 'S.A.S.'),
                                      ('S.A.', 'S.A.'),
                                      ('LTDA.', 'LTDA.'),
                                      ('ENTIDAD PRIVADA', 'ENTIDAD PRIVADA'),
                                      ('ENTIDAD ORDEN NACIONAL', 'ENTIDAD ORDEN NACIONAL'),
                                      ('ENTIDAD ORDEN TERRITORIAL', 'ENTIDAD ORDEN TERRITORIAL'),
                                      ('ENTIDAD EXTRANJERA', 'ENTIDAD EXTRANJERA'),
                                      ('ENTIDAD SIN ÁNIMO DE LUCRO', 'ENTIDAD SIN ÁNIMO DE LUCRO'),
                                      ('EMPRESA INDUSTRIAL Y COMERCIAL DEL ESTADO', 'EMPRESA INDUSTRIAL Y COMERCIAL DEL ESTADO'),
                                      ('ORGANIZACIÓN ECONOMÍA SOLIDARIA', 'ORGANIZACIÓN ECONOMÍA SOLIDARIA'),
                                      ('SOCIEDAD EN COMANDITA POR ACCIONES', 'SOCIEDAD EN COMANDITA POR ACCIONES'),
                                      ('S.A. IPS', 'S.A. IPS'),
                                      ('S.A. E.S.P.', 'S.A. E.S.P.'),
                                      ('E.S.P.', 'E.S.P.'),
                                      ('& CIA. SCA.', '& CIA. SCA.'),
                                      ('CIA S.EN C.', 'CIA S.EN C.')], string="Naturaleza de la compañía", tracking=True)
    field_1 = fields.Many2one('address.code', tracking=True)
    field_2  = fields.Char('Campo direccion 2', tracking=True)
    field_3 = fields.Selection([('A', 'A'),
                                      ('B', 'B'),
                                      ('C', 'C'),
                                      ('D', 'D'),
                                      ('E', 'E'),
                                      ('F', 'F'),
                                      ('G', 'G'),
                                      ('H', 'H'),
                                      ('I', 'I'),
                                      ('J', 'J'),
                                      ('K', 'K'),
                                      ('L', 'L'),
                                      ('M', 'M'),
                                      ('N', 'N'),
                                      ('Ñ', 'Ñ'),
                                      ('O', 'O'),
                                      ('P', 'P'),
                                      ('Q', 'Q'),
                                      ('R', 'R'),
                                      ('S', 'S'),
                                      ('T', 'T'),
                                      ('U', 'U'),
                                      ('V', 'V'),
                                      ('W', 'W'),
                                      ('X', 'X'),
                                      ('Y', 'Y'),
                                      ('Z', 'Z'),
                                      ], string="Campo dirección 3", tracking=True)
    field_4 = fields.Many2one('street.code', tracking=True)
    field_5  = fields.Char('Campo direccion 5', tracking=True)
    field_6 = fields.Selection([('A', 'A'),
                                      ('B', 'B'),
                                      ('C', 'C'),
                                      ('D', 'D'),
                                      ('E', 'E'),
                                      ('F', 'F'),
                                      ('G', 'G'),
                                      ('H', 'H'),
                                      ('I', 'I'),
                                      ('J', 'J'),
                                      ('K', 'K'),
                                      ('L', 'L'),
                                      ('M', 'M'),
                                      ('N', 'N'),
                                      ('Ñ', 'Ñ'),
                                      ('O', 'O'),
                                      ('P', 'P'),
                                      ('Q', 'Q'),
                                      ('R', 'R'),
                                      ('S', 'S'),
                                      ('T', 'T'),
                                      ('U', 'U'),
                                      ('V', 'V'),
                                      ('W', 'W'),
                                      ('X', 'X'),
                                      ('Y', 'Y'),
                                      ('Z', 'Z'),
                                      ], string="Campo dirección 6", tracking=True)
    field_7 = fields.Many2one('street.code', tracking=True)
    field_8  = fields.Char('Campo direccion 8', tracking=True)
    field_9 = fields.Many2one('address.code', tracking=True)
    field_10  = fields.Char('Campo direccion 10', tracking=True)
    field_11 = fields.Many2one('address.code', tracking=True)
    field_12  = fields.Char('Campo direccion 12', tracking=True)
    street_thomas=fields.Char('Dirección aux', default='.')
    street = fields.Char(compute='_compute_street')
    city_crm = fields.Many2one('res.city', string='Ciudad', domain="[('state_id', '=?', state_id)]", required=False, placeholder='Ciudad')
    city=fields.Char(invisible=True)

    vat=fields.Char(required=False, tracking=True)
    l10n_co_document_type = fields.Selection([('rut', 'NIT'),
                                              ('id_card', 'Tarjeta de Identidad'),
                                              ('passport', 'Pasaporte'),
                                              ('foreign_id_card', 'Cédula Extranjera'),
                                              ('external_id', 'ID del Exterior'),
                                              ('diplomatic_card', 'Carné Diplomatico'),
                                              ('residence_document', 'Salvoconducto de Permanencia'),
                                              ('civil_registration', 'Registro Civil'),
                                              ('national_citizen_id', 'Cédula de ciudadanía')], string='Document Type',
                                             help='Indicates to what document the information in here belongs to.', required=False)
    nit  = fields.Char('NIT')
    dv = fields.Selection([('0', '0'),
                                      ('1', '1'),
                                      ('2', '2'),
                                      ('3', '3'),
                                      ('4', '4'),
                                      ('5', '5'),
                                      ('6', '6'),
                                      ('7', '7'),
                                      ('8', '8'),
                                      ('9', '9')
                                      ], string="DV", tracking=True, required=False)
    ciiu = fields.Many2many('ciiu.value', string="CIIU")
    rut  = fields.Binary('RUT', tracking=True)
    sarlaf_document  = fields.Binary('Documentación SARGLAFT', tracking=True)
    file_name = fields.Char("File Name")
    file_name_sarlaf = fields.Char("File Name")

    main_road = fields.Many2one('adress.contact', string="Vía principal")
    main_road_name=fields.Char('Nombre vía principal', placeholder='38A BIS')
    generating_route = fields.Char('Vía generadora:', placeholder='20B')
    #farm = fields.Char('Predio', required='False', placeholder='61')
    complement_adress = fields.Char('Complemento', placeholder='SUR')

    full_adress = fields.Char('Dirección Completa')
    lang = fields.Selection(required=True, string='Idioma')
    res_lang_id = fields.Many2one('res.lang', invisible=True)
    indicative_state = fields.Integer('Indicativo Provincia', compute='_get_indicative_state')
    indicative_country = fields.Integer('Indicativo País', related='country_id.phone_code')
    consult_order = fields.Selection([('REPORTADO', 'REPORTADO'),
                                      ('NO REPORTADO', 'NO REPORTADO')], string="Consulta lista restrictiva", tracking=True)
    #email = fields.Char(company_dependent=True)
    email = fields.Char(company_dependent=False, required=False)

    fecha_consulta = fields.Date(tracking=True, string='Fecha de consulta')
    approval_compliance = fields.Selection([('SI', 'SI'),
                                            ('NO', 'NO'),
                                            ('NO APLICA', 'NO APLICA')], string="Aprobación Oficial de cumplimiento", tracking=True)

    risk_profile= fields.Selection([('ALTO', 'ALTO'),
                                      ('MEDIO', 'MEDIO'),
                                      ('BAJO', 'BAJO')], string="Perfil de riesgo", tracking=True)
    risk_percentage = fields.Float('Porcentaje de riesgo', tracking=True)

    customer_type = fields.Selection([('PROSPECTO', 'PROSPECTO'),
                                      ('ACTUAL', 'ACTUAL'),
                                      ('INACTIVO', 'INACTIVO')], string="Tipo de cliente", tracking=True)
    departure_date = fields.Date('Fecha de salida', tracking=True)
    sector = fields.Selection([('PÚBLICO', 'PÚBLICO'),
                                      ('PRIVADO', 'PRIVADO'),
                                      ('MIXTO', 'MIXTO')], string="Sector")
    fecha_creacion = fields.Datetime('Fecha de creación', tracking=True)
    date_update = fields.Datetime('Fecha de Actualización de datos', tracking=True)
    billing_potencial = fields.Selection([('1M-10M', '1M-10M'),
                                      ('10M-20M', '10M-20M'),
                                      ('20M-50M', '20M-50M'),
                                      ('50M-100M', '50M-100M'),
                                      ('100M-500M', '100M-500M'),
                                      ('MÁS DE 500M', 'MÁS DE 500M')], string="Potencial de Facturación")

    rol = fields.Selection([('user', 'USUARIO'),
                           ('evaluate', 'EVALUA'),
                           ('influence', 'INFLUENCIA'),
                           ('decides', 'DECIDE'),
                           ('approves', 'APRUEBA')], string="Rol")
    attitude = fields.Selection([('PADRINO', 'PADRINO'),
                           ('AMIGO', 'AMIGO'),
                           ('NEUTRAL', 'NEUTRAL'),
                           ('OPOSITOR', 'OPOSITOR'),
                           ('ENEMIGO', 'ENEMIGO')], string="Actitud")
    street_contact = fields.Char('Dirección completa')
    field_contact_1 = fields.Many2one('address.code', tracking=True)
    field_contact_2  = fields.Char('Campo direccion 2', tracking=True)
    field_contact_3 = fields.Selection([('A', 'A'),
                                      ('B', 'B'),
                                      ('C', 'C'),
                                      ('D', 'D'),
                                      ('E', 'E'),
                                      ('F', 'F'),
                                      ('G', 'G'),
                                      ('H', 'H'),
                                      ('I', 'I'),
                                      ('J', 'J'),
                                      ('K', 'K'),
                                      ('L', 'L'),
                                      ('M', 'M'),
                                      ('N', 'N'),
                                      ('Ñ', 'Ñ'),
                                      ('O', 'O'),
                                      ('P', 'P'),
                                      ('Q', 'Q'),
                                      ('R', 'R'),
                                      ('S', 'S'),
                                      ('T', 'T'),
                                      ('U', 'U'),
                                      ('V', 'V'),
                                      ('W', 'W'),
                                      ('X', 'X'),
                                      ('Y', 'Y'),
                                      ('Z', 'Z'),
                                      ], string="Campo dirección 3", tracking=True)
    field_contact_4 = fields.Many2one('street.code', tracking=True)
    field_contact_5  = fields.Char('Campo direccion 5', tracking=True)
    field_contact_6 = fields.Selection([('A', 'A'),
                                      ('B', 'B'),
                                      ('C', 'C'),
                                      ('D', 'D'),
                                      ('E', 'E'),
                                      ('F', 'F'),
                                      ('G', 'G'),
                                      ('H', 'H'),
                                      ('I', 'I'),
                                      ('J', 'J'),
                                      ('K', 'K'),
                                      ('L', 'L'),
                                      ('M', 'M'),
                                      ('N', 'N'),
                                      ('Ñ', 'Ñ'),
                                      ('O', 'O'),
                                      ('P', 'P'),
                                      ('Q', 'Q'),
                                      ('R', 'R'),
                                      ('S', 'S'),
                                      ('T', 'T'),
                                      ('U', 'U'),
                                      ('V', 'V'),
                                      ('W', 'W'),
                                      ('X', 'X'),
                                      ('Y', 'Y'),
                                      ('Z', 'Z'),
                                      ], string="Campo dirección 6", tracking=True)
    field_contact_7 = fields.Many2one('street.code', tracking=True)
    field_contact_8  = fields.Char('Campo direccion 8', tracking=True)
    field_contact_9 = fields.Many2one('address.code', tracking=True)
    field_contact_10  = fields.Char('Campo direccion 10', tracking=True)
    field_contact_11 = fields.Many2one('address.code', tracking=True)
    field_contact_12  = fields.Char('Campo direccion 12', tracking=True)
    website_id = fields.Many2one('website', ondelete='cascade', string="Website")
    check_colombia=fields.Boolean('Seleccion Colombia', compute='check_colombia_id')
    check_type_contact=fields.Boolean('Tipo de contacto', compute='onchange_check_type_contact', invisible='True')
    check_tittle=fields.Boolean('titulo check', compute='_check_title', invisible='True')
    check_parent_id = fields.Boolean(invisible=True, compute='_compute_checK_parent_id_contact')

    user_id = fields.Many2one('res.users', string='Salesperson', company_dependent=True,
      help='The internal user in charge of this contact.')

  # concatenar nombre completo del empleado o nombre de la empresa
    # @api.onchange('company_type','company_name','company_nature','first_name', 'last_name', 'middle_name', 'second_last_name')
    # def _onchange_nombre_completo(self):
    #         if  self.company_type=='person':
    #             self.name = "%s %s %s %s" % (
    #             self.firts_name if self.firts_name else "",
    #             self.last_name if self.last_name else "",
    #             self.middle_name if self.middle_name else "",
    #             self.second_last_name if self.second_last_name else "")
    #         else:
    #             self.name = "%s %s" % (
    #             self.company_name if self.company_name else "",
    #             self.company_nature if self.company_nature else "")
    
    @api.onchange('company_type','company_name','company_nature')
    def _onchange_nombre_completo(self):
            if self.company_type == 'company' and (self.company_nature or self.company_name):
                self.name = "%s %s" % (
                self.company_name if self.company_name else "",
                self.company_nature if self.company_nature else "")

    @api.onchange('type')
    def onchange_check_type_contact(self):
            if  self.type=='contact':
                self.check_type_contact=True
            else:
                self.check_type_contact=False

    @api.depends('field_1','field_2','field_3','field_4', 'field_5', 'field_6', 'field_7',
                  'field_8', 'field_9', 'field_10', 'field_11', 'field_12', 'country_id')
    def _compute_street(self):
        for record in self:
            record.street = "%s %s %s %s %s %s %s %s %s %s %s %s" % (
                record.field_1.code if record.field_1.code else "",
                record.field_2 if record.field_2 else "",
                record.field_3 if record.field_3 else "",
                record.field_4.name if record.field_4.name else "",
                record.field_5 if record.field_5 else "",
                record.field_6 if record.field_6 else "",
                record.field_7.name if record.field_7.name else "",
                record.field_8 if record.field_8 else "",
                record.field_9.code if record.field_9.code else "",
                record.field_10 if record.field_10 else "",
                record.field_11.code if record.field_11.code else "",
                record.field_12 if record.field_12 else ""
            )

    ##### Agregar archivo rut a adjuntos
    @api.model
    def create(self, vals):
        if vals.get('parent_id') and vals.get('type') and vals.get('type') == 'contact':
            parent = self.browse(vals.get('parent_id'))
            vals.update(field_1=parent.field_1.id if parent.field_1 else False)
            vals.update(field_2=parent.field_2)
            vals.update(field_3=parent.field_3)
            vals.update(field_4=parent.field_4.id)
            vals.update(field_5=parent.field_5)
            vals.update(field_6=parent.field_6)
            vals.update(field_7=parent.field_7.id)
            vals.update(field_8=parent.field_8)
            vals.update(field_9=parent.field_9.id)
            vals.update(field_10=parent.field_10)
            vals.update(field_11=parent.field_11.id)
            vals.update(field_12=parent.field_12)
        

        res = super(ResPartner, self).create(vals)

        if vals.get('rut') and vals.get('file_name'):
                dic = {
                    'name': vals.get('file_name'),
                    'datas': vals.get('rut'),
                    'res_model': 'res.partner',
                    'res_id': res.id
                }
                self.env['ir.attachment'].create(dic)
        if vals.get('sarlaf_document') and vals.get('file_name_sarlaf'):
                dic = {
                    'name': vals.get('file_name_sarlaf'),
                    'datas': vals.get('sarlaf_document'),
                    'res_model': 'res.partner',
                    'res_id': res.id
                }
                self.env['ir.attachment'].create(dic)
        return res

    def write(self, vals):

        if vals.get('sarlaf_document'):
            vals['date_update']=fields.Datetime.now()

        if vals.get('parent_id') and vals.get('type') and vals.get('type') == 'contact':
            parent = self.browse(vals.get('parent_id'))
            vals.update(field_1=parent.field_1.id if parent.field_1 else False)
            vals.update(field_2=parent.field_2)
            vals.update(field_3=parent.field_3)
            vals.update(field_4=parent.field_4.id)
            vals.update(field_5=parent.field_5)
            vals.update(field_6=parent.field_6)
            vals.update(field_7=parent.field_7.id)
            vals.update(field_8=parent.field_8)
            vals.update(field_9=parent.field_9.id)
            vals.update(field_10=parent.field_10)
            vals.update(field_11=parent.field_11.id)
            vals.update(field_12=parent.field_12)
        res = super(ResPartner, self).write(vals)

        for record in self:
            if vals.get('rut') and vals.get('file_name'):
                dic = {
                    'name': vals.get('file_name'),
                    'datas': vals.get('rut'),
                    'res_model': 'res.partner',
                    'res_id': record.id
                }
                self.env['ir.attachment'].create(dic)
            if vals.get('sarlaf_document') and vals.get('file_name_sarlaf'):
                dic = {
                    'name': vals.get('file_name_sarlaf'),
                    'datas': vals.get('sarlaf_document'),
                    'res_model': 'res.partner',
                    'res_id': record.id
                }
                self.env['ir.attachment'].create(dic)
        return res

    @api.depends('country_id')
    def check_colombia_id(self):
        for line in self:
            if line.country_id.name == 'Colombia':
                self.check_colombia = True
            else:
                self.check_colombia = False

    def _check_title(self):
        for line in self:
            line.check_tittle = self.env.user.has_group('contacts_thomas.group_admin')


    @api.depends('state_id')
    def _get_indicative_state(self):
        for line in self:
            line.indicative_state = line.state_id.indicative_state_code

    @api.constrains('company_type', 'child_ids')
    def _check_child(self):
        for record in self:
            if record.company_type == 'company' and not record.child_ids:
                raise ValidationError("Es necesario registrar por lo menos un contacto en esta compañía")

    @api.depends('company_name')
    def _get_customer_name(self):
        for line in self:
            line.name = line.company_name

    @api.depends('parent_id','type')
    def _compute_checK_parent_id_contact(self):
        for line in self:
            if line.parent_id and line.type=='contact':
                line.check_parent_id=True
            else:
                line.check_parent_id=False

    @api.onchange('city_id')
    def _onchange_city_state_country(self):
        for record in self:
            if record.city_id:
                record.state_id = record.city_id.state_id
                record.country_id = record.city_id.country_id
            else:
                record.state_id = False
                record.country_id = False
