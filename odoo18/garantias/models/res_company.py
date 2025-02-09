import logging
from odoo import api, models

_logger = logging.getLogger(__name__)

class ResCompany(models.Model):
    _inherit = 'res.company'

    @api.model
    def get_parent_company_location(self):
        """
        Obtiene la latitud y longitud de la compañía padre del usuario activo.

        Retorna:
            dict: {'lat': float, 'lng': float} - Coordenadas de la compañía padre o actual.
        """
        user = self.env.user
        user_company = user.company_id

        # Obtener compañía padre o la actual si no hay una superior
        parent_company = user_company.parent_id or user_company

        if parent_company.partner_id:
            latitude = parent_company.partner_id.partner_latitude or 0.0
            longitude = parent_company.partner_id.partner_longitude or 0.0

            _logger.info(
                f"Usuario {user.name} (ID: {user.id}) obtuvo la ubicación de la compañía: "
                f"Lat: {latitude}, Lng: {longitude}"
            )

            return {'lat': latitude, 'lng': longitude}

        _logger.warning(f"Usuario {user.name} (ID: {user.id}) intentó acceder a una ubicación no disponible.")
        return {'lat': 0.0, 'lng': 0.0}