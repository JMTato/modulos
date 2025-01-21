from odoo import http
from odoo.http import request

class GarantiaController(http.Controller):
    @http.route('/garantia/get_api_key', type='json', auth='user')
    def get_google_maps_api_key(self):
        """Devuelve la API Key de Google Maps a la vista"""
        api_key = request.env['ir.config_parameter'].sudo().get_param('google_maps_api_key')
        return {'api_key': api_key}