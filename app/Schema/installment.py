from marshmallow import fields, validate, pre_load
from marshmallow import Schema


class BaseSchema(Schema):
    @pre_load
    def normalize_keys(self, data, **kwargs):
        if isinstance(data, dict):
            return {k.upper(): v for k, v in data.items()}
        return data


class InstallmentSchema(BaseSchema):
    id = fields.Int(data_key="ID", attribute="id", required=True)
    numero = fields.Int(data_key="NUMERO", attribute="numero", required=True)
    valor = fields.Float(data_key="VALOR", attribute="valor", required=True)
    vencimento = fields.Str(data_key="VENCIMENTO", attribute="vencimento", required=True)
    pago = fields.Bool(data_key="PAGO", attribute="pago", required=False, missing=False)
    control_id = fields.Int(data_key="CONTROL_ID", attribute="control_id", required=False, allow_none=True)
