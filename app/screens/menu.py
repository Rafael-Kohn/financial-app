from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from app.utils.env_utils import save_gemini_key
from app.utils.notify import Notify

class MenuScreen(Screen):
    def abrir_registrar_api(self):
        layout = BoxLayout(orientation="vertical", padding=10, spacing=10)
        label = Label(text="Digite sua GEMINI_API_KEY:")
        api_input = TextInput(multiline=False, size_hint_y=None, height=40)
        btn_box = BoxLayout(size_hint_y=None, height=40, spacing=10)
        salvar_btn = Button(text="Salvar")
        cancelar_btn = Button(text="Cancelar")

        btn_box.add_widget(salvar_btn)
        btn_box.add_widget(cancelar_btn)
        layout.add_widget(label)
        layout.add_widget(api_input)
        layout.add_widget(btn_box)

        popup = Popup(title="Registrar Chave API", content=layout, size_hint=(0.8, 0.4))

        def salvar_chave(instance):
            try:
                save_gemini_key(api_input.text)
                Notify.push("notice", "Chave salva com sucesso")
                popup.dismiss()
            except Exception as e:
                Notify.push("error", f"Erro: {e}")

        salvar_btn.bind(on_release=salvar_chave)
        cancelar_btn.bind(on_release=lambda x: popup.dismiss())

        popup.open()
    
