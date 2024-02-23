from datetime import datetime, date, timedelta

from odoo import api, fields, models, _

class FleetDocument(models.Model):
    _name = 'fleet.document'
    _description = 'Vencimientos de documentos vehiculos'

    name = fields.Char(string='Nombre de Documento', required=True, copy=False, help="Ingrese nombre de Documento")             
    
    document_id = fields.Char(string='Tipo de Documento del Vehiculo',required=True)
    description = fields.Text(string='Descripción', copy=False, help="Descripción del documento")
    expiry_date = fields.Date(string='Fecha de vencimiento', copy=False, help="Elija Fecha de vencimiento")
    fleet_id = fields.Many2one('fleet.vehicle', copy=False, string="Vehiculo",help="Elija el empleado")
    doc_attachment_ids = fields.Many2many(
        'ir.attachment',
        'fleet_document_ir_attachment_rel',  # Cambia este nombre a algo único
        'fleet_document_id',  # Cambia este nombre a algo único
        'ir_attachment_id',
        string="Adjuntar",
        help='Puedes adjuntar aquí el documento al vehículo',
        copy=False
    )

    issue_date = fields.Date(string='Fecha de creación',default=fields.Date.context_today, copy=False,
                help="Aquí va la fecha de creación del documento, por lo general se usa el dia de actual")


    # Metodos
    def mail_reminder(self):
        for doc in self.search([]):
            if doc.expiry_date:
                if (datetime.now() + timedelta(days=1)).date() >= (
                        doc.expiry_date - timedelta(days=7)):
                    mail_content = ("  Hola, el documento del Vehiculo  " + str(
                        doc.fleet_id.model_id) + ",<br>Con Matricula " + str(
                        doc.fleet_id.license_plate) + "<br>" + "<br> Por favor, ingrese al sistema y actualice este documento que vence el " + \
                                    str(doc.expiry_date) + "<br> Gracias"
                                                           "")
                    main_content = {
                        'subject': _('El Documento %s se vence el %s') % (
                            str(doc.name), str(doc.expiry_date)),
                        'author_id': self.env.user.partner_id.id,
                        'body_html': mail_content,
                        'email_to': doc.fleet_id.manager_id.work_email,
                        
                    }
                    self.env['mail.mail'].create(main_content).send()

    @api.onchange('expiry_date')
    def check_expr_date(self):
        """Function to obtain a validation error for expired documents."""
        if self.expiry_date and self.expiry_date < date.today():
            return {
                'warning': {
                    'title': _('Documento vencido.'),
                    'message': _("El documento esta vencido.")
                }
            }


class Fleet(models.Model):
    """Inherit the 'fleet' module to add 'Documents' super button."""
    _inherit = 'fleet.vehicle'

    document_count = fields.Integer(compute='_compute_document_count',string='# Documentos',help="Obtene el total de documentos del empleado")

    #Compute contador
    def _compute_document_count(self):
        """Function to obtain the total count of documents."""
        for rec in self:
            rec.document_count = self.env['fleet.document'].search_count(
                [('fleet_id', '=', rec.id)])

    
    def document_view(self):
        self.ensure_one()
        return {
            'name': _('Documentos'),
            'domain': [('fleet_id', '=', self.id)],
            'res_model': 'fleet.document',
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'view_type': 'form',
            'help': _('''<p class="oe_view_nocontent_create">
                           Hace click en NUEVO para subir un documento.
                        </p>'''),
            'limit': 80,
            'context': {'default_fleet_id': self.id}
        }


class ResUser(models.Model):
    _inherit = 'res.users'

    email = fields.Char(string='Email del Usuario',required=True)