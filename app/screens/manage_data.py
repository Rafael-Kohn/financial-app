from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivy.app import App

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from app.utils.formatter import format_currency, format_date
from app.utils.notify import Notify


class ManageDataScreen(Screen):
    tipo_selecao = ObjectProperty(None)
    lista_box = ObjectProperty(None)
    status_label = ObjectProperty(None)

    def on_pre_enter(self):
        self.carregar("gastos")

    # -----------------------------------
    # CARREGAR LISTAS
    # -----------------------------------
    def carregar(self, tipo):
        self.lista_box.clear_widgets()
        self.status_label.text = ""

        app = App.get_running_app()

        if tipo == "gastos":
            for g in app.expense_service.list():
                self._linha_gasto(g)

        elif tipo == "cartoes":
            for c in app.card_service.list():
                self._linha_cartao(c)

        elif tipo == "categorias":
            for cat in app.category_service.list():
                self._linha_categoria(cat)

    # -----------------------------------
    # LINHAS
    # -----------------------------------
    def _linha_gasto(self, g):
        linha = BoxLayout(size_hint_y=None, height=40, spacing=10)

        linha.add_widget(Label(text=f"{format_date(g.data_recorrencia)}- {g.nome}: {format_currency(g.valor)} - {g.tipo} [{g.categoria}]"))

        btn_edit = Button(text="Editar", size_hint_x=None, width=80)
        btn_edit.bind(on_release=lambda x: self.editar_gasto(g))
        linha.add_widget(btn_edit)

        btn_del = Button(text="Excluir", size_hint_x=None, width=80)
        btn_del.bind(on_release=lambda x: self.deletar_gasto(g))
        linha.add_widget(btn_del)

        self.lista_box.add_widget(linha)

    def _linha_cartao(self, c):
        linha = BoxLayout(size_hint_y=None, height=40, spacing=10)

        linha.add_widget(Label(text=f"{c.apelido} ({c.banco}) - {c.ultimos_digitos}"))

        btn_edit = Button(text="Editar", size_hint_x=None, width=80)
        btn_edit.bind(on_release=lambda x: self.editar_cartao(c))
        linha.add_widget(btn_edit)

        btn_del = Button(text="Excluir", size_hint_x=None, width=80)
        btn_del.bind(on_release=lambda x: self.deletar_cartao(c))
        linha.add_widget(btn_del)

        self.lista_box.add_widget(linha)

    def _linha_categoria(self, cat):
        linha = BoxLayout(size_hint_y=None, height=40, spacing=10)

        linha.add_widget(Label(text=f"{cat.nome}"))

        btn_edit = Button(text="Editar", size_hint_x=None, width=80)
        btn_edit.bind(on_release=lambda x: self.editar_categoria(cat))
        linha.add_widget(btn_edit)

        btn_del = Button(text="Excluir", size_hint_x=None, width=80)
        btn_del.bind(on_release=lambda x: self.deletar_categoria(cat))
        linha.add_widget(btn_del)

        self.lista_box.add_widget(linha)

    # -----------------------------------
    # DELETE
    # -----------------------------------
    def deletar_gasto(self, g):
        app = App.get_running_app()
        app.expense_service.delete(g.id)
        Notify.push("notice", "Gasto removido")
        self.carregar("gastos")

    def deletar_cartao(self, c):
        app = App.get_running_app()
        app.card_service.delete(c.id)
        Notify.push("notice", "Cartão removido")
        self.carregar("cartoes")

    def deletar_categoria(self, cat):
        app = App.get_running_app()
        app.category_service.delete(cat.id)
        Notify.push("notice", "Categoria removida")
        self.carregar("categorias")

    # -----------------------------------
    # EDIT
    # -----------------------------------
    def editar_gasto(self, g):
        tela = self.manager.get_screen("edit_gasto")
        tela.selected_item = g
        self.manager.current = "edit_gasto"

    def editar_cartao(self, c):
        tela = self.manager.get_screen("edit_cartao")
        tela.selected_item = c
        self.manager.current = "edit_cartao"

    def editar_categoria(self, cat):
        tela = self.manager.get_screen("edit_categoria")
        tela.selected_item = cat
        self.manager.current = "edit_categoria"
