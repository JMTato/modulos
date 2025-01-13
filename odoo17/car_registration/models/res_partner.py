from odoo import models, fields

class ResPartner(models.Model):
    _inherit = "res.partner"

    vehicle_count = fields.Integer(
        string="Número de Vehículos",
        compute="_compute_vehicle_count"
    )

    def _compute_vehicle_count(self):
        """Cuenta la cantidad de vehículos asociados al cliente."""
        for partner in self:
            partner.vehicle_count = self.env["fleet.vehicle"].search_count(
                [("driver_id", "=", partner.id)]
            )

    def action_view_partner_vehicles(self):
        """Muestra la vista de los vehículos del cliente."""
        return {
            "type": "ir.actions.act_window",
            "name": "Vehículos del Cliente",
            "res_model": "fleet.vehicle",
            "view_mode": "tree,form",
            "domain": [("driver_id", "=", self.id)],
            "context": {"default_driver_id": self.id},
        }