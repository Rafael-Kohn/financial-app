from marshmallow import fields, validate, pre_load
from marshmallow import Schema


class BaseSchema(Schema):
    @pre_load
    def normalize_keys(self, data, **kwargs):
        if isinstance(data, dict):
            return {k.upper(): v for k, v in data.items()}
        return data


class ControlSchema(BaseSchema):
    id = fields.Int(data_key="ID", attribute="id", required=True)
    nome = fields.Str(data_key="NOME", attribute="nome", required=True)
    tipo = fields.Str(data_key="TIPO", attribute="tipo", required=True, validate=validate.Length(min=1))
    valor = fields.Float(data_key="VALOR", attribute="valor", required=True)
    forma = fields.Str(data_key="FORMA", attribute="forma", required=True)
    parcelas = fields.Int(data_key="PARCELAS", attribute="parcelas", required=False, missing=1)
    data = fields.Str(data_key="DATA", attribute="data", required=False, allow_none=True)
    cartao_id = fields.Int(data_key="CARTAO_ID", attribute="cartao_id", required=False, allow_none=True)
    modo = fields.Str(data_key="MODO", attribute="modo", required=False, allow_none=True)
    status = fields.Str(data_key="STATUS", attribute="status", required=False, missing="ativo")
