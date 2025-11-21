# app/screens/analysis.py
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty, ListProperty, StringProperty
from app.services.expense_service import ExpenseService
from app.services.gemini_service import ask_gemini
from app.utils.formatter import format_currency
from datetime import datetime, timedelta
from app.widgets.datepicker import DatePicker
from app.widgets.expense_table import ExpenseTable


class AnalysisScreen(Screen):
    # Widgets do KV
    chat_input = ObjectProperty(None)
    chat_output = ObjectProperty(None)
    expense_table = ObjectProperty(None)
    filtro_data_inicio = ObjectProperty(None)
    filtro_data_fim = ObjectProperty(None)
    filtro_categoria = ObjectProperty(None)
    filtro_tipo = ObjectProperty(None)

    # Listas para spinners
    categorias = ListProperty([])
    tipos = ListProperty([])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.expense_service = ExpenseService()
        self.filtered_expenses = []

    def on_pre_enter(self):
        all_expenses = self.expense_service.list()

        # Preencher opções dos filtros
        categorias = list({g.categoria for g in all_expenses if g.categoria})
        tipos = list({g.tipo for g in all_expenses if g.tipo})
        self.categorias = ["All"] + categorias
        self.tipos = ["All"] + tipos

        # Filtros default
        hoje = datetime.today()
        inicio_default = (hoje - timedelta(days=30)).strftime("%d/%m/%Y")
        fim_default = hoje.strftime("%d/%m/%Y")

        self.filtro_data_inicio.text = inicio_default
        self.filtro_data_fim.text = fim_default
        self.filtro_categoria.text = "All"
        self.filtro_tipo.text = "All"

        self.apply_filters()

    # ---------------- DatePicker ----------------
    def show_datepicker_inicio(self):
        DatePicker(callback=self.set_data_inicio).open()

    def show_datepicker_fim(self):
        DatePicker(callback=self.set_data_fim).open()

    def set_data_inicio(self, date_str):
        self.filtro_data_inicio.text = date_str
        self.apply_filters()

    def set_data_fim(self, date_str):
        self.filtro_data_fim.text = date_str
        self.apply_filters()

    # ---------------- Filtros ----------------
    def apply_filters(self):
        all_expenses = self.expense_service.list()

        inicio = self._parse_date(getattr(self.filtro_data_inicio, 'text', None))
        fim = self._parse_date(getattr(self.filtro_data_fim, 'text', None))
        categoria = getattr(self.filtro_categoria, 'text', 'All').strip()
        tipo = getattr(self.filtro_tipo, 'text', 'All').strip()

        filtered = []
        for exp in all_expenses:
            g_data = self._parse_date(exp.data_recorrencia)
            if not g_data:
                continue  # pula despesas sem data válida

            if inicio and g_data < inicio:
                continue
            if fim and g_data > fim:
                continue
            if categoria != "All" and categoria.lower() != exp.categoria.lower():
                continue
            if tipo != "All" and tipo.lower() != exp.tipo.lower():
                continue
            filtered.append(exp)

        self.filtered_expenses = filtered
        self._update_table()

    def _parse_date(self, s):
        if not s:
            return None
        for fmt in ("%d/%m/%Y", "%d-%m-%Y"):
            try:
                return datetime.strptime(s, fmt)
            except:
                continue
        return None

    # ---------------- Atualização da tabela ----------------
    def _update_table(self):
        if not self.expense_table:
            return
        self.expense_table.update_data(self.filtered_expenses)

    # ---------------- Chat Gemini ----------------
    def conversar(self):
        if not self.chat_input:
            return

        prompt_user = self.chat_input.text.strip()
        if not prompt_user:
            return

        table_txt = "\n".join(
            f"{g.nome}: {format_currency(g.valor)} [{g.tipo} | {g.categoria} | {g.data_recorrencia}]"
            for g in self.filtered_expenses
        )

        prompt = f"Você é um analista financeiro. Aqui estão os dados filtrados:\n{table_txt}\nResponda direto: {prompt_user}"
        resposta = ask_gemini(prompt)
        if self.chat_output:
            self.chat_output.text = resposta
