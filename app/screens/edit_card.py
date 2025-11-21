from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivy.app import App
from app.utils.notify import Notify

class EditCardScreen(Screen):
    banco = ObjectProperty(None)
    responsavel = ObjectProperty(None)
    apelido = ObjectProperty(None)
    ultimos_digitos = ObjectProperty(None)

    def on_pre_enter(self):
        card = self.selected_item

        self.banco.text = card.banco
        self.responsavel.text = card.responsavel
        self.apelido.text = card.apelido
        self.ultimos_digitos.text = card.ultimos_digitos

    def salvar(self):
        u = self.ultimos_digitos.text.strip()

        if len(u) != 4 or not u.isdigit():
            Notify.push("warning", "Últimos dígitos inválidos")
            return

        app = App.get_running_app()
        card = self.selected_item

        app.card_service.update(
            card.id,
            self.banco.text.strip(),
            self.responsavel.text.strip(),
            self.apelido.text.strip(),
            u
        )

        Notify.push("notice", "Cartão atualizado")
        self.manager.current = "manage_data"
