from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from app.services.finance_service import gerar_resumo_gastos
from app.services.gemini_service import ask_gemini

class AnalysisScreen(Screen):
    chat_input = ObjectProperty(None)
    chat_output = ObjectProperty(None)

    contexto_pronto = False

    def on_pre_enter(self):
        if not self.contexto_pronto:
            self.chat_output.text = "Carregando contexto..."
            self.iniciar_contexto()

    def iniciar_contexto(self):
        resumo = gerar_resumo_gastos()
        ask_gemini("Você é um analista financeiro. Resuma tudo direto: " + resumo)
        self.contexto_pronto = True
        self.chat_output.text = "Contexto carregado."

    def conversar(self):
        p = self.chat_input.text.strip()
        if not p:
            return

        r = ask_gemini("Responda direto: " + p)
        self.chat_output.text = r
