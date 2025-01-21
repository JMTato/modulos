from odoo import api, models

class ResCompany(models.Model):
    _inherit = 'res.company'

    @api.model
    def get_parent_company_location(self):
        """Obtiene la latitud y longitud de la compañía padre del usuario activo."""
        user_company = self.env.user.company_id
        parent_company = user_company.parent_id or user_company  # Obtener compañía padre o actual

        if parent_company.partner_id:
            return {
                'lat': parent_company.partner_id.partner_latitude or 0.0,
                'lng': parent_company.partner_id.partner_longitude or 0.0,
            }
        return {'lat': 0.0, 'lng': 0.0}