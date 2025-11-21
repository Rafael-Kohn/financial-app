from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivy.app import App
from datetime import datetime
from ..widgets.datepicker import DatePicker

class AddExpenseScreen(Screen): 
    cartao = ObjectProperty(None)
    tipo = ObjectProperty(None)
    valor = ObjectProperty(None)
    parcelas = ObjectProperty(None)
    data_recorrencia = ObjectProperty(None)
    frequencia = ObjectProperty(None)
    nome = ObjectProperty(None)
    categoria = ObjectProperty(None)
    status_label = ObjectProperty(None)  # opcional: mostre mensagens ao usuário

    def on_pre_enter(self):
        app = App.get_running_app()

        # preencher cartões via service
        cards = app.card_service.list()
        if cards:
            self.cartao.values = [f"{c.id} - {c.apelido}" for c in cards]
        else:
            self.cartao.values = ["Nenhum cartão"]

        # preencher categorias via service (Spinner)
        cats = app.category_service.list()
        if cats:
            self.categoria.values = [c.nome for c in cats]
            # seleciona 1ª categoria por padrão
            if not self.categoria.text or self.categoria.text == "Categoria":
                self.categoria.text = cats[0].nome
        else:
            self.categoria.values = ["Sem categorias"]
            self.categoria.text = "Sem categorias"

    def salvar_gasto(self):
        app = App.get_running_app()

        # validações básicas
        if not self.cartao.text or "Nenhum" in self.cartao.text:
            self._status("Selecione um cartão.")
            return

        try:
            cartao_id = int(self.cartao.text.split(" - ")[0])
        except Exception:
            self._status("Cartão inválido.")
            return

        try:
            valor = float(self.valor.text.replace(",", "."))
        except Exception:
            self._status("Valor inválido.")
            return

        parcelas = int(self.parcelas.text) if (self.parcelas.text and self.parcelas.text.isdigit()) else 1

        categoria = self.categoria.text if self.categoria.text and self.categoria.text not in ("Sem categorias", "Categoria") else ""

        # chama service (ele cuida do parcelamento)
        try:
            app.expense_service.create(
                cartao_id=cartao_id,
                tipo=self.tipo.text or "",
                valor=valor,
                parcelas=parcelas,
                data_recorrencia=self.data_recorrencia.text or datetime.now().strftime("%d/%m/%Y"),
                frequencia=self.frequencia.text or "",
                nome=self.nome.text or "",
                categoria=categoria
            )
        except Exception as e:
            self._status(f"Erro: {e}")
            return

        self._status("Gasto salvo.")
        # limpa campos se quiser
        self.valor.text = ""
        self.parcelas.text = ""
        self.nome.text = ""
        # volta ao menu
        self.manager.current = "menu"

    def data_hoje(self):
        return datetime.now().strftime("%d/%m/%Y")

    def formatar_data(self, campo):
        texto = campo.text.replace("/", "")
        if len(texto) > 8:
            texto = texto[:8]

        novo = ""
        if len(texto) >= 2:
            novo += texto[:2] + "/"
        if len(texto) >= 4:
            novo += texto[2:4] + "/"
        if len(texto) > 4:
            novo += texto[4:]
        campo.text = novo
        campo.cursor = (len(campo.text), 0)

    def abrir_calendario(self):
        popup = DatePicker(callback=self.setar_data)
        popup.open()

    def setar_data(self, data):
        # assume id=data_recorrencia presente no kv
        self.ids.data_recorrencia.text = data

    def _status(self, msg):
        # se tiver status_label definido no kv, atualiza; senão ignora
        try:
            if self.status_label:
                self.status_label.text = msg
            else:
                self.ids.status_label.text = msg
        except Exception:
            pass
