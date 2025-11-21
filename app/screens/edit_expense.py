from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivy.app import App
from ..utils.notify import Notify
from ..models.expense import Expense
from datetime import datetime
from ..widgets.datepicker import DatePicker


class EditExpenseScreen(Screen):
    cartao = ObjectProperty(None)
    tipo = ObjectProperty(None)
    valor = ObjectProperty(None)
    parcelas = ObjectProperty(None)
    data_recorrencia = ObjectProperty(None)
    frequencia = ObjectProperty(None)
    nome = ObjectProperty(None)
    categoria = ObjectProperty(None)

    selected_item = None  # vem da ManageDataScreen
    def abrir_calendario(self):
        popup = DatePicker(callback=self.setar_data)
        popup.open()

    def setar_data(self, data):
        self.data_recorrencia.text = data

    def on_pre_enter(self):
        app = App.get_running_app()
        e = self.selected_item

        # preencher cartões no spinner
        cards = app.card_service.list()
        if cards:
            self.cartao.values = [f"{c.id} - {c.apelido}" for c in cards]
            self.cartao.text = f"{e.cartao_id} - {app.card_service.get(e.cartao_id).apelido}"
        else:
            self.cartao.values = ["Nenhum cartão"]
            self.cartao.text = "Nenhum cartão"

        # preencher categorias
        cats = app.category_service.list()
        if cats:
            self.categoria.values = [c.nome for c in cats]
            self.categoria.text = e.categoria
        else:
            self.categoria.values = ["Sem categorias"]
            self.categoria.text = "Sem categorias"

        # preencher demais campos
        self.tipo.text = e.tipo
        self.valor.text = str(e.valor)
        self.parcelas.text = str(e.parcelas)
        self.data_recorrencia.text = e.data_recorrencia or datetime.now().strftime("%d/%m/%Y")
        self.frequencia.text = e.frequencia or ""
        self.nome.text = e.nome

    # ---------------------------------------------------
    # SALVAR
    # ---------------------------------------------------
    def salvar(self):
        app = App.get_running_app()

        # validar cartão
        if not self.cartao.text or "Nenhum" in self.cartao.text:
            Notify.push("warning", "Selecione um cartão.")
            return

        try:
            cartao_id = int(self.cartao.text.split(" - ")[0])
        except:
            Notify.push("warning", "Cartão inválido.")
            return

        # validar valor
        try:
            valor = float(self.valor.text.replace(",", "."))
        except:
            Notify.push("warning", "Valor inválido.")
            return

        # parcelas
        if self.parcelas.text.isdigit():
            parcelas = int(self.parcelas.text)
        else:
            parcelas = 1

        categoria = self.categoria.text if self.categoria.text not in ("Sem categorias", "Categoria") else ""

        e = self.selected_item

        atualizado = Expense(
            cartao_id=cartao_id,
            tipo=self.tipo.text or "",
            valor=valor,
            parcelas=parcelas,
            data_recorrencia=self.data_recorrencia.text,
            frequencia=self.frequencia.text or "",
            nome=self.nome.text or "",
            categoria=categoria,
            id=e.id
        )

        atualizado.save()
        Notify.push("notice", "Gasto atualizado")
        self.manager.current = "manage_data"
