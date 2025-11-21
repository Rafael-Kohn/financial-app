# services/expense_service.py
from ..utils import database
from datetime import datetime

def _add_months(dt, months):
    # adiciona months a dt sem depender de dateutil
    month = dt.month - 1 + months
    year = dt.year + month // 12
    month = month % 12 + 1
    day = min(dt.day, [31,
                       29 if (year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)) else 28,
                       31,30,31,30,31,31,30,31,30,31][month-1])
    return datetime(year, month, day)

class ExpenseService:
    def create(self, cartao_id, tipo, valor, parcelas,
               data_recorrencia, frequencia, nome, categoria):
        """
        Se parcelas > 1, cria uma entrada por parcela com datas incrementadas por mês.
        """
        if isinstance(valor, str):
            valor = float(valor.replace(",", "."))
        else:
            valor = float(valor or 0)

        parcelas = int(parcelas or 1)
        if not data_recorrencia:
            data_recorrencia = datetime.now().strftime("%d/%m/%Y")

        try:
            data_dt = datetime.strptime(data_recorrencia, "%d/%m/%Y")
        except Exception:
            data_dt = datetime.now()

        if parcelas <= 1:
            database.create_gasto(cartao_id, tipo, valor, parcelas,
                                  data_dt.strftime("%d/%m/%Y"), frequencia, nome, categoria)
        else:
            # dividir com arredondamento na última parcela
            parcela_val = round(valor / parcelas, 2)
            soma = 0.0
            for i in range(parcelas):
                if i == parcelas - 1:
                    v = round(valor - soma, 2)
                else:
                    v = parcela_val
                    soma += v
                dt_parc = _add_months(data_dt, i)
                database.create_gasto(cartao_id, tipo, v, parcelas,
                                      dt_parc.strftime("%d/%m/%Y"), frequencia,
                                      f"{nome} (parc {i+1}/{parcelas})", categoria)

    def list(self):
        return database.read_gastos()

    def get(self, id):
        gastos = database.read_gastos()
        for g in gastos:
            if g.id == id:
                return g
        return None

    def update(self, id, cartao_id, tipo, valor, parcelas, data_recorrencia, frequencia, nome, categoria):
        database.update_gasto(id, cartao_id, tipo, valor, parcelas, data_recorrencia, frequencia, nome, categoria)

    def delete(self, id):
        database.delete_gasto(id)
