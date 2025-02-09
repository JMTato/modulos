from odoo import models, fields

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    eficiencia_combustible = fields.Char(string="Eficiencia Combustible")
    agarre_mojado = fields.Char(string="Agarre Mojado")
    ruido = fields.Char(string="Ruido")
