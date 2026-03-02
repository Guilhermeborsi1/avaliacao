from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Avaliacao(models.Model):
    _name = "avaliacao.avaliacao"
    _description = "Avaliação de Desempenho"

    imagem_1920 = fields.Image(string="Imagem")
    name = fields.Char(string="Nome da peça", required=True)
    code = fields.Char(string="Código da peça", required=True)
    description = fields.Text(string="Descrição da peça")
    evaluation_criteria = fields.Text(string="Critérios de avaliação")

    resistance_score = fields.Float(string="Ponto por Resistência", required=True)
    durability_score = fields.Float(string="Ponto por Durabilidade", required=True)
    termal_resistance_score = fields.Float(string="Ponto por Resistência Térmica", required=True)
    fatigue_resistance_score = fields.Float(string="Ponto por Resistência à Fadiga", required=True)
    misuse_resistance_score = fields.Float(string="Ponto por Resistência ao Uso Indevido", required=True)

    contract = fields.Binary(string="Contrato", required=True)
    report = fields.Binary(string="Relatório", required=True)
    date_avaliation = fields.Date(string="Data da Avaliação", required=True)

    product_tmpl_id = fields.Many2one(
        comodel_name="product.template",
        string="Produto",
        required=True,
        ondelete="cascade",
        index=True,
    )

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

    partner_id = fields.Many2one(
        comodel_name="res.partner",
        string="Cliente",
        ondelete="set null",
        index=True,
    )

    user_id = fields.Many2one(
        comodel_name="res.users",
        string="Responsável tecnico",
        ondelete="set null",
        index=True,
        domain=[("share", "=", False)],
        default=lambda self: self.env.user,
    )

    # -------------------------
    # Cálculo
    # -------------------------
    @api.depends(
        "resistance_score",
        "durability_score",
        "termal_resistance_score",
        "fatigue_resistance_score",
        "misuse_resistance_score",
        "product_tmpl_id",
    )
    def _compute_score(self):
        for rec in self:
            rec.score_total = (
                (rec.resistance_score or 0)
                + (rec.durability_score or 0)
                + (rec.termal_resistance_score or 0)
                + (rec.fatigue_resistance_score or 0)
                + (rec.misuse_resistance_score or 0)
            )
            rec.aproved = rec.score_total >= 60

    # -------------------------
    # Sincronização com produto
    # -------------------------
    def _sync_produto_aprovacao(self):
        """Empurra o status atual de aprovado para o produto vinculado."""
        for rec in self:
            if rec.product_tmpl_id:
                rec.product_tmpl_id.x_aprovado_avaliacao = rec.aproved

    @api.model
    def create(self, vals):
        rec = super().create(vals)
        # garante sync mesmo se já vier aprovado e só depois vincular produto
        rec._sync_produto_aprovacao()
        return rec

    def write(self, vals):
        res = super().write(vals)

        campos_que_afetam = {
            "product_tmpl_id",
            "resistance_score",
            "durability_score",
            "termal_resistance_score",
            "fatigue_resistance_score",
            "misuse_resistance_score",
        }
        if campos_que_afetam.intersection(vals.keys()):
            self._sync_produto_aprovacao()

        return res

    @api.onchange("product_tmpl_id")
    def _onchange_product_tmpl_id(self):
        # Atualiza “na hora” no formulário (UX)
        if self.product_tmpl_id:
            self.product_tmpl_id.x_aprovado_avaliacao = self.aproved

    # -------------------------
    # Validação (somente valida)
    # -------------------------
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