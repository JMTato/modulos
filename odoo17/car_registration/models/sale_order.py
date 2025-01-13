from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = "sale.order"

    vehicle_id = fields.Many2one(
        "fleet.vehicle",
        string="Vehículo",
        domain="[('driver_id', '=', partner_id)]",
        help="Selecciona un vehículo asociado al cliente."
    )

    vehicle_license_plate = fields.Char(
        string="Matrícula"
    )

    vehicle_kilometers = fields.Integer(
        string="Kilómetros"
    )

    @api.onchange("vehicle_id")
    def _onchange_vehicle_id(self):
        """Al seleccionar un vehículo, se actualizan los datos."""
        if self.vehicle_id:
            self.vehicle_license_plate = self.vehicle_id.license_plate or ""
            self.vehicle_kilometers = int(self.vehicle_id.odometer or 0)
        else:
            self.vehicle_license_plate = ""
            self.vehicle_kilometers = 0