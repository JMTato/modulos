from odoo import models

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def _create_invoices(self, grouped=False, final=False):
        invoices = super(SaleOrder, self)._create_invoices(grouped, final)
        for order in self:
            for line in order.order_line:
                invoice_line = line.invoice_lines.filtered(lambda l: l.move_id in invoices)
                invoice_line.write({
                    'eficiencia_combustible': line.eficiencia_combustible,
                    'agarre_mojado': line.agarre_mojado,
                    'ruido': line.ruido,
                })
        return invoices
