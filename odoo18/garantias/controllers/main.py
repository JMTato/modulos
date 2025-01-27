from odoo import http
from odoo.http import request
import logging

_logger = logging.getLogger(__name__)

class GarantiaController(http.Controller):
    @http.route('/garantia/get_api_key', type='json', auth='user')
    def get_google_maps_api_key(self):
        """Devuelve la API Key de Google Maps a la vista, solo para usuarios autenticados"""
        try:
            user = request.env.user
            _logger.info("Solicitud de API Key por el usuario: %s (ID: %s)", user.name, user.id)
            
            api_key = request.env['ir.config_parameter'].sudo().get_param('google_maps_api_key')
            
            if not api_key:
                _logger.warning("API Key no configurada - Usuario: %s (ID: %s)", user.name, user.id)
                return {'error': 'API Key no configurada, contacte al administrador.'}
            
            return {'api_key': api_key}
        
        except Exception as e:
            _logger.error("Error al obtener la API Key de Google Maps: %s", str(e))
            return {'error': 'Ocurrió un error inesperado, contacte al administrador.'}