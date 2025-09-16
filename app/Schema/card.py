from marshmallow import Schema, fields, validates, ValidationError, pre_load
from marshmallow import validate


class BaseSchema(Schema):
    @pre_load
    def normalize_keys(self, data, **kwargs):
        # aceita tanto "id" quanto "ID" e normaliza para UPPERCASE (para casar com data_key abaixo)
        if isinstance(data, dict):
            return {k.upper(): v for k, v in data.items()}
        return data


class CardSchema(BaseSchema):
    id = fields.Int(data_key="ID", attribute="id", required=True)
    nome = fields.Str(data_key="NOME", attribute="nome", required=True, validate=validate.Length(min=1))
    proprietario = fields.Str(data_key="PROPRIETARIO", attribute="proprietario", required=True)
    ultimos_digitos = fields.Str(
        data_key="ULTIMOS_DIGITOS",
        attribute="ultimos_digitos",
        required=True,
        validate=validate.Length(equal=4)
    )
