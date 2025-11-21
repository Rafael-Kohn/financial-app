from ..models.expense import Expense
from ..utils.formatter import format_currency

def gerar_resumo_gastos():
    gastos = Expense.get_all()

    if not gastos:
        return "Nenhum gasto registrado."

    txt = "Resumo dos gastos:\n"
    for g in gastos:
        txt += f"- {g.nome}: {format_currency(g.valor)} [{g.categoria}]\n"

    return txt
