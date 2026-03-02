from odoo import models, fields

class ProductTemplate(models.Model):
    _inherit = "product.template"

    x_aprovado_avaliacao = fields.Boolean(
        string="Aprovado na Avaliação",
        readonly=True,
        default=False)    
