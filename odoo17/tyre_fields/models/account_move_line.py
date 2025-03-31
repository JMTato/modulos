from odoo import models, fields, api

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    eficiencia_combustible = fields.Char(string='Eficiencia Combustible', readonly=False)
    agarre_mojado = fields.Char(string='Agarre Mojado', readonly=False)
    ruido = fields.Char(string='Ruido', readonly=False)

    @api.onchange('product_id')
    def _onchange_product_id_set_tyre_fields(self):
        """Cargar automáticamente los campos del producto, pero permitir edición manual."""
        if self.product_id:
            self.eficiencia_combustible = self.product_id.eficiencia_combustible or ''
            self.agarre_mojado = self.product_id.agarre_mojado or ''
            self.ruido = self.product_id.ruido or ''
