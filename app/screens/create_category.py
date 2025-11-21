from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from app.services.category_service import CategoryService
from app.utils.notify import Notify
import sqlite3

class CategoryCreateScreen(Screen):
    input_nome = ObjectProperty(None)

    def salvar(self):
        nome = self.input_nome.text.strip()

        if nome == "":
            Notify.push("warning", "Digite um nome para a categoria.")
            return

        try:
            CategoryService().create(nome)
            Notify.push("notice", "Categoria criada com sucesso.")
            self.input_nome.text = ""  # limpa o campo

        except sqlite3.IntegrityError:
            Notify.push("warning", "Já existe uma categoria com esse nome.")

        except Exception as e:
            Notify.push("error", str(e))
