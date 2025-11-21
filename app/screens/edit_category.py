from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivy.app import App
from ..utils.notify import Notify

class EditCategoryScreen(Screen):
    nome = ObjectProperty(None)

    def on_pre_enter(self):
        app = App.get_running_app()
        cat = self.selected_item

        self.nome.text = cat.nome

    def salvar(self):
        novo = self.nome.text.strip()
        if not novo:
            Notify.push("warning", "Nome obrigatório")
            return

        app = App.get_running_app()
        cat = self.selected_item
        app.category_service.update(cat.id, novo)

        Notify.push("notice", "Categoria atualizada")
        self.manager.current = "manage_data"
