from kivy.uix.recycleview import RecycleView
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout

class ExpenseRow(BoxLayout):
    cartao = StringProperty("")
    nome = StringProperty("")
    valor = StringProperty("")
    tipo = StringProperty("")
    categoria = StringProperty("")
    data_recorrencia = StringProperty("")


class ExpenseTable(RecycleView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data = []

    def update_data(self, expenses):
        self.data = [
            {
                "cartao": str(getattr(exp, "cartao", "")),
                "nome": str(getattr(exp, "nome", "")),
                "valor": str(getattr(exp, "valor", "")),
                "tipo": str(getattr(exp, "tipo", "")),
                "categoria": str(getattr(exp, "categoria", "")),
                "data_recorrencia": str(getattr(exp, "data_recorrencia", "")),
            }
            for exp in expenses
        ]
