#models/garantias_settins.py
from odoo import api, fields, models

class GarantiasSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    google_maps_api_key = fields.Char(
        string="Google Maps API Key",
        config_parameter='garantias.google_maps_api_key',
        help="Introduce la clave de API de Google Maps para la geolocalización automática."
    )