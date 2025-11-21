from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.floatlayout import FloatLayout
from kivy.lang import Builder

from app.models.card import Card
from app.models.category import Category
from app.models.expense import Expense

from app.services.card_service import CardService
from app.services.category_service import CategoryService
from app.services.expense_service import ExpenseService
from app.services.excel_service import export_to_excel
from app.services.finance_service import gerar_resumo_gastos
from app.services.gemini_service import ask_gemini

from app.utils import init_db, Notify, format_currency

from app.screens.menu import MenuScreen
from app.screens.add_card import AddCardScreen
from app.screens.add_expense import AddExpenseScreen
from app.screens.manage_data import ManageDataScreen
from app.screens.analysis import AnalysisScreen
from app.screens.create_category import CategoryCreateScreen
from app.screens.edit_category import EditCategoryScreen
from app.screens.edit_card import EditCardScreen
from app.screens.edit_expense import EditExpenseScreen
from app.utils.env_utils import save_gemini_key




class FinancialApp(App):
    def build(self):

        # >>>>>>>>>>>>>>>>>>>>>>>>>>>
        Builder.load_file("main.kv")
        # <<<<<<<<<<<<<<<<<<<<<<<<<<<

        init_db()

        self.card_service = CardService()
        self.category_service = CategoryService()
        self.expense_service = ExpenseService()

        root = FloatLayout()

        self.sm = ScreenManager()
        self.sm.add_widget(MenuScreen(name="menu"))
        self.sm.add_widget(CategoryCreateScreen(name="criar_categoria"))
        self.sm.add_widget(AddCardScreen(name="add_card"))
        self.sm.add_widget(AddExpenseScreen(name="add_expense"))
        self.sm.add_widget(ManageDataScreen(name="manage_data"))
        self.sm.add_widget(AnalysisScreen(name="analysis"))
        self.sm.add_widget(EditCategoryScreen(name="edit_categoria"))
        self.sm.add_widget(EditCardScreen(name="edit_cartao"))
        self.sm.add_widget(EditExpenseScreen(name="edit_gasto"))

        root.add_widget(self.sm)

        self.notification_layer = FloatLayout(size_hint=(1, 1))
        root.add_widget(self.notification_layer)
        Notify.setup(self.notification_layer)

        return root
        
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

if __name__ == "__main__":
    FinancialApp().run()
