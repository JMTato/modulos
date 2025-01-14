from odoo import models, fields

class PosOrder(models.Model):
    _inherit = 'pos.order'

    hide_prices = fields.Boolean(string="Hide Prices on Ticket", default=False)