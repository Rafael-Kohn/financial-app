from ..models.expense import Expense
from ..utils.formatter import format_currency,format_date

def gerar_resumo_gastos():
    gastos = Expense.get_all()

    if not gastos:
        return "Nenhum gasto registrado."

    txt = "Resumo dos gastos:\n"
    for g in gastos:
        txt += f"{format_date(g.data_recorrencia)}- {g.nome}: {format_currency(g.valor)} - {g.tipo} [{g.categoria}]\n"

    return txt
