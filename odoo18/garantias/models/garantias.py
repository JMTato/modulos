import logging
from odoo import api, fields, models, _
import requests

_logger = logging.getLogger(__name__)

class Garantias(models.Model):
    _name = 'garantias'
    _description = 'Registro de Garantías'

    name = fields.Char(
        string='Referencia',
        required=True,
        copy=False,
        readonly=True,
        default=lambda self: self.env['ir.sequence'].next_by_code('garantias.reference')
    )

    cliente_nombre = fields.Char(string='Nombre completo', required=True)
    nif = fields.Char(string='NIF')
    movil = fields.Char(string='Móvil')

    calle = fields.Char(string='Calle')
    ciudad = fields.Char(string='Ciudad')
    cp = fields.Char(string='C.P.')
    country_id = fields.Many2one('res.country', string='País')

    latitude = fields.Float(string='Latitud', digits=(16, 5))
    longitude = fields.Float(string='Longitud', digits=(16, 5))

    ubicacion = fields.Char(
        string='Ubicación',
        compute='_compute_ubicacion',
        store=True
    )

    fecha_registro = fields.Date(
        string='Fecha de Registro', 
        default=fields.Date.context_today
    )

    company_id = fields.Many2one(
        'res.company',
        string='Compañía',
        default=lambda self: self.env.company
    )

    barcode = fields.Char(string='Código de Barras')
    imagen_equipo = fields.Image(string='Foto del Equipo')

    @api.depends('calle', 'ciudad', 'cp', 'country_id')
    def _compute_ubicacion(self):
        """Calcula la ubicación concatenando los campos de dirección."""
        for record in self:
            parts = [
                record.calle or '',
                record.ciudad or '',
                record.cp or '',
                record.country_id.name or ''
            ]
            record.ubicacion = ', '.join(filter(None, parts))

    def geo_localize(self):
        """Obtiene la latitud y longitud usando la API de geolocalización de Google."""
        for record in self:
            if record.ubicacion:
                try:
                    # Obtener la clave de API de Google desde la configuración correcta
                    api_key = self.env['ir.config_parameter'].sudo().get_param('base_geolocalize.google_map_api_key')

                    if not api_key:
                        _logger.error("No se ha configurado la clave de API de Google Maps en ir.config_parameter.")
                        continue

                    # Llamada a la API de Google Maps para geolocalizar la dirección
                    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={record.ubicacion}&key={api_key}"
                    response = requests.get(url)
                    result = response.json()

                    if result.get('status') == 'OK':
                        location = result['results'][0]['geometry']['location']
                        record.latitude = location['lat']
                        record.longitude = location['lng']
                        _logger.info(f"Geolocalización exitosa: Lat {record.latitude}, Lon {record.longitude}")
                    else:
                        _logger.warning(f"No se pudieron obtener coordenadas para: {record.ubicacion}")
                        record.latitude = 0.0
                        record.longitude = 0.0

                except Exception as e:
                    _logger.error(f"Error en la geolocalización: {e}")
                    record.latitude = 0.0
                    record.longitude = 0.0

    @api.model
    def create(self, vals):
        """Sobrescribe create para calcular latitud y longitud al crear el registro."""
        record = super(Garantias, self).create(vals)
        record.geo_localize()
        return record

    def write(self, vals):
        """Sobrescribe write para actualizar latitud y longitud si se modifica la ubicación."""
        result = super(Garantias, self).write(vals)
        if 'calle' in vals or 'ciudad' in vals or 'cp' in vals or 'country_id' in vals:
            self.geo_localize()
        return result

    def action_geo_localize(self):
        """Acción para el botón de geolocalización."""
        self.geo_localize()
        return {
            'effect': {
                'fadeout': 'slow',
                'message': _('Ubicación actualizada correctamente.'),
                'type': 'rainbow_man',
            }
        }