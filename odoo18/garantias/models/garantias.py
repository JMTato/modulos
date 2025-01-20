from odoo import models, fields, api

class Garantia(models.Model):
    _name = 'garantia.registro'
    _description = 'Registro de Garantías'
    _rec_name = 'referencia'

    referencia = fields.Char(
        string='Referencia', 
        required=True, 
        copy=False, 
        readonly=True, 
        default=lambda self: self.env['ir.sequence'].next_by_code('garantia.registro')
    )
    nombre_completo = fields.Char(string='Nombre Completo', required=True)
    nif = fields.Char(string='NIF')
    movil = fields.Char(string='Móvil')
    calle = fields.Char(string='Calle')
    numero = fields.Integer(string='Número')
    ciudad = fields.Char(string='Ciudad')
    cp = fields.Char(string='Código Postal')
    pais_id = fields.Many2one('res.country', string='País', required=True)
    company_id = fields.Many2one('res.company', string='Compañía', default=lambda self: self.env.company)
    fecha_registro = fields.Date(string='Fecha de Registro', default=fields.Date.context_today)
    ubicacion = fields.Char(string='Ubicación', compute='_compute_ubicacion', store=True)
    codigo_barras = fields.Char(string='Código de Barras')
    imagenes = fields.Binary(string='Fotos del equipo')

    @api.depends('calle', 'numero', 'ciudad', 'cp', 'pais_id')
    def _compute_ubicacion(self):
        for record in self:
            if record.calle and record.numero and record.ciudad and record.cp and record.pais_id:
                record.ubicacion = f"{record.calle}, {record.numero}, {record.ciudad}, {record.cp}, {record.pais_id.name}"
            else:
                record.ubicacion = ''