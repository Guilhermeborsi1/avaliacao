from odoo import models, fields

class ProductTemplate(models.Model):
    _inherit = "product.template"

    x_aprovado_avaliacao = fields.Boolean(
        string="Aprovado na Avaliação",
        readonly=True,
        default=False)    

    x_ponto_por_resistencia = fields.Float(
        string="Ponto por Resistência",
        readonly=True,
        default=0.0)
    x_ponto_por_durabilidade = fields.Float(
        string="Ponto por Durabilidade",
        readonly=True,
        default=0.0)
    x_ponto_por_resistencia_termica = fields.Float(
        string="Ponto por Resistência Térmica",
        readonly=True,      
        default=0.0)
    x_ponto_por_resistencia_e_fadiga = fields.Float(
        string="Ponto por Resistência à Fadiga",
        readonly=True,
        default=0.0)    
    x_ponto_por_resistencia_ao_uso_indevido = fields.Float(
        string="Ponto por Resistência ao Uso Indevido",
        readonly=True,
        default=0.0)    