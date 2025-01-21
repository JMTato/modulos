# models/garantias.py
import requests
from odoo import api, fields, models

class Garantias(models.Model):
    _name = 'garantias'
    _description = 'Registro de Garantías'

    # ----------------------------------------
    # Definición de campos del modelo
    # ----------------------------------------

    # Campo de referencia: se obtiene mediante una secuencia al crear el registro
    name = fields.Char(
        string='Referencia',
        required=True,
        copy=False,
        readonly=True,
        default=lambda self: self.env['ir.sequence'].next_by_code('garantias.reference')
    )

    # Datos del cliente
    cliente_nombre = fields.Char(string='Nombre completo', required=True)
    nif = fields.Char(string='NIF')
    movil = fields.Char(string='Móvil')

    # Dirección
    calle = fields.Char(string='Calle')
    numero = fields.Integer(string='Número')
    ciudad = fields.Char(string='Ciudad')
    cp = fields.Char(string='C.P.')
    
    # País (relación con res.country para desplegable de países)
    country_id = fields.Many2one('res.country', string='País')

    # Compañía asociada al usuario que crea el registro (readonly)
    company_id = fields.Many2one(
        'res.company',
        string='Compañía',
        default=lambda self: self.env.company,
        readonly=True
    )

    # Fecha de registro: se llena automáticamente con la fecha actual
    fecha_registro = fields.Date(
        string='Fecha',
        default=fields.Date.context_today,
        readonly=True
    )

    # Campo calculado para almacenar la ubicación concatenada
    ubicacion = fields.Char(
        string='Ubicación',
        compute='_compute_ubicacion',
        store=True
    )

    # Campos de geolocalización (latitud y longitud)
    latitude = fields.Float(string='Latitud')
    longitude = fields.Float(string='Longitud')

    # Código de barras del equipo
    barcode = fields.Char(string='Código de barras')

    # Foto del equipo (almacenada en formato binario)
    imagen_equipo = fields.Image(string='Foto del equipo')

    # ----------------------------------------
    # Métodos del modelo
    # ----------------------------------------

    @api.depends('calle', 'numero', 'ciudad', 'cp', 'country_id')
    def _compute_ubicacion(self):
        """Calcula la ubicación concatenando los campos de dirección."""
        for record in self:
            parts = []
            if record.calle:
                parts.append(record.calle)
            if record.numero:
                parts.append(str(record.numero))
            if record.ciudad:
                parts.append(record.ciudad)
            if record.cp:
                parts.append(record.cp)
            if record.country_id:
                parts.append(record.country_id.name)

            record.ubicacion = ', '.join(parts)

    # ----------------------------------------
    # Métodos para la geolocalización
    # ----------------------------------------

    def _google_geocode(self, address):
        """Devuelve (lat, lng) usando la API de geocodificación de Google."""
        if not address:
            return (0.0, 0.0)

        api_key = self._get_google_maps_api_key()
        if not api_key:
            # Si la clave de API no está configurada, retorna coordenadas vacías
            return (0.0, 0.0)

        # URL de la API de geocodificación de Google Maps
        url = 'https://maps.googleapis.com/maps/api/geocode/json'
        params = {
            'address': address,
            'key': api_key
        }
        try:
            # Realizar la solicitud HTTP a la API de Google Maps
            resp = requests.get(url, params=params, timeout=5)
            if resp.status_code == 200:
                data = resp.json()
                if data.get('status') == 'OK':
                    # Obtener latitud y longitud del primer resultado encontrado
                    results = data.get('results', [])
                    if results:
                        location = results[0]['geometry']['location']
                        return (location['lat'], location['lng'])
        except Exception as e:
            # Manejar errores de conexión u otros problemas
            pass

        return (0.0, 0.0)

    def _get_google_maps_api_key(self):
        """Obtiene la clave API de Google Maps desde la configuración estándar de Odoo."""
        return self.env['ir.config_parameter'].sudo().get_param('google_maps_api_key', default='')

    # ----------------------------------------
    # Sobreescritura de métodos de creación/modificación
    # ----------------------------------------

    @api.model
    def create(self, vals):
        """
        Sobreescribe el método create para calcular latitud/longitud automáticamente 
        cuando se crea un registro de garantía con dirección.
        """
        if 'calle' in vals or 'numero' in vals or 'ciudad' in vals or 'cp' in vals or 'country_id' in vals:
            # Construir dirección antes de la geocodificación
            address = f"{vals.get('calle', '')} {vals.get('numero', '')}, {vals.get('ciudad', '')}, {vals.get('cp', '')}, {self.env['res.country'].browse(vals.get('country_id')).name or ''}"
            lat, lng = self._google_geocode(address)
            vals['latitude'] = lat
            vals['longitude'] = lng

        return super(Garantias, self).create(vals)

    def write(self, vals):
        """
        Sobreescribe el método write para actualizar latitud/longitud 
        automáticamente cuando se actualiza la dirección de una garantía.
        """
        if 'calle' in vals or 'numero' in vals or 'ciudad' in vals or 'cp' in vals or 'country_id' in vals:
            for record in self:
                address = f"{vals.get('calle', record.calle)} {vals.get('numero', record.numero)}, {vals.get('ciudad', record.ciudad)}, {vals.get('cp', record.cp)}, {record.country_id.name}"
                lat, lng = self._google_geocode(address)
                vals['latitude'] = lat
                vals['longitude'] = lng

        return super(Garantias, self).write(vals)