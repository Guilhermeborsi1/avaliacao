from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Avaliacao(models.Model):
    _name = "avaliacao.avaliacao"
    _description = "Avaliação de Desempenho"
    imagem_1920 = fields.Image(string="Imagem") 
    name = fields.Char(string = "Nome da peça" , required=True)
    code = fields.Char(string = "Código da peça" , required=True)
    description = fields.Text(string = "Descrição da peça")
    evaluation_criteria = fields.Text(string = "Critérios de avaliação")
    resistance_score = fields.Float(string = "Ponto por Resistência" , required=True)
    durability_score = fields.Float(string = "Ponto por Durabilidade" , required=True)
    termal_resistance_score = fields.Float(string = "Ponto por Resistência Térmica" , required=True)
    fatigue_resistance_score = fields.Float(string = "Ponto por Resistência à Fadiga" , required=True)
    misuse_resistance_score = fields.Float(string = "Ponto por Resistência ao Uso Indevido" , required=True)
    contract = fields.Binary(string = "Contrato", required=True)
    report = fields.Binary(string = "Relatório", required=True)
    date_avaliation = fields.Date(string = "Data da Avaliação", required=True)
    score_total = fields.Float(
        string="Pontuação Final",
        compute="_compute_score",
        store=True,
    )

    aproved = fields.Boolean(
        string="Aprovado",
        compute="_compute_score",
        store=True,
    )

    
    @api.depends(
        "resistance_score",
        "durability_score",
        "termal_resistance_score",
        "fatigue_resistance_score",
        "misuse_resistance_score",
    )
    def _compute_score(self):
        for rec in self:
            rec.score_total = (
            +(rec.resistance_score or 0)
            +(rec.durability_score or 0)
            +(rec.termal_resistance_score or 0)
            +(rec.fatigue_resistance_score or 0)
            +(rec.misuse_resistance_score or 0)
            )
            rec.aproved = rec.score_total >= 60

    @api.constrains(
        "resistance_score",
        "durability_score",
        "termal_resistance_score",
        "fatigue_resistance_score",
        "misuse_resistance_score",
    )
    def _check_positive_scores(self):
        for rec in self:
            for field_name in [
                "resistance_score",
                "durability_score",
                "termal_resistance_score",
                "fatigue_resistance_score",
                "misuse_resistance_score",
            ]:
                score = rec[field_name]
                if score is not None and (score < 0 or score > 20):
                    raise ValidationError("As pontuações devem estar entre 0 e 20.")